import json
import numpy as np
import comms as co

#Input file

with open("input.json", "r") as inputFile:
	scData = json.load(inputFile)

co.fileConv(scData)

#Outputs (have to write a function in comms.py to calculate each of these values)

scPower = co.SItodB(scData["Spacecraft"]["Power"]["Value"])
scGain = co.calcGain(scData["Mission"]["FrequencyDownlink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["Antenna"]["Efficiency"]["Value"])
scPointLoss = co.calcPointingLoss(scData["Mission"]["FrequencyDownlink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["OffsetPointing"]["Value"], scData["Spacecraft"]["Antenna"]["HalfPowerAngle"]["Value"])
scTransLoss = co.SItodB(scData["Spacecraft"]["LossFactor"]["Value"])

gsGain = co.calcGain(scData["Mission"]["FrequencyDownlink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["Antenna"]["Efficiency"]["Value"])
gsPointLoss = co.calcPointingLoss(scData["Mission"]["FrequencyDownlink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["OffsetPointing"]["Value"], scData["GroundStation"]["Antenna"]["HalfPowerAngle"]["Value"])
gsRecLoss = co.SItodB(scData["GroundStation"]["LossFactor"]["Value"])

systemNoiseTemp = co.calcSystemNoise(scData["Mission"]["FrequencyDownlink"]["Value"], "downlink")

transmissionPathLoss = co.calcTransPathLoss(scData["Mission"]["FrequencyDownlink"]["Value"])
print(transmissionPathLoss)
freeSpaceLoss = co.calcSpaceLoss(scData["Mission"]["Planet"], scData["Mission"]["FrequencyDownlink"]["Value"], scData["Mission"]["OrbitingBodyRadius"]["Value"], scData["Mission"]["OrbitalHeight"]["Value"], scData["Mission"]["SpacecraftSunDistance"]["Value"], scData["Mission"]["ElongationAngle"]["Value"])

transmissionDataRate = co.calcTransmissionDataRate(scData["Payload"], scData["Mission"])

snr = scPower + scTransLoss + scGain + transmissionPathLoss + gsGain + freeSpaceLoss + scPointLoss + gsPointLoss + gsRecLoss + 228.6 - 10*np.log10(transmissionDataRate) - 10*np.log10(systemNoiseTemp)
snrReq = scData["PayloadRequirements"] 

print(f'Based on the data inputed the Eb/n0 ratio is {snr} dB. The required Eb/n0 ratio is {snrReq} dB. This leaves a margin of {snr-snrReq}') 			#It is assumed that the SNR = Eb/nO, in other words that bitrate = bandwidth noise, don't forget the 3dB margin
print("Note: The margin should be at least 3dB to ensure the robustness of the system.")