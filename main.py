import json
import numpy as np
import comms as co

#Input file

with open("input.json", "r") as inputFile:
	scData = json.load(inputFile)

co.fileConv(scData)

#Inputs

# print(scData["Spacecraft"]["LossFactor"]["Value"])

# scPower = co.SIConv(scData["Spacecraft"]["Power"])
# scTransLoss = co.SIConv(scData["Spacecraft"]["LossFactor"])
# gsRecLoss = co.SIConv(scData["GroundStation"]["LossFactor"])
# scSignalFrequency = co.SIConv(scData["Spacecraft"]["Frequency"])

#Outputs (have to write a function in comms.py to calculate each of these values)

scPower = scData["Spacecraft"]["Power"]["Value"]
scGain = co.calcGain(scData["Mission"]["FrequencyDownlink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["Antenna"]["Efficiency"]["Value"])
scPointLoss = co.calcPointingLoss(scData["Mission"]["FrequencyDownlink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["OffsetPointing"]["Value"], scData["Spacecraft"]["Antenna"]["HalfPowerAngle"]["Value"])
scTransLoss = scData["Spacecraft"]["LossFactor"]["Value"]

gsGain = co.calcGain(scData["Mission"]["FrequencyDownlink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["Antenna"]["Efficiency"]["Value"])
gsPointLoss = co.calcPointingLoss(scData["Mission"]["FrequencyDownlink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["OffsetPointing"]["Value"], scData["GroundStation"]["Antenna"]["HalfPowerAngle"]["Value"])
gsRecLoss = scData["GroundStation"]["LossFactor"]["Value"]

systemNoiseTemp = co.calcSystemNoise(scData["Mission"]["FrequencyDownlink"]["Value"], "downlink")

transmissionPathLoss = -10


freeSpaceLoss = -10

dataRate = 10



snr = scPower + scTransLoss + scGain + transmissionPathLoss + gsGain + freeSpaceLoss + scPointLoss + gsPointLoss + gsRecLoss + 228.6 - 10*np.log(dataRate) - 10*np.log(systemNoiseTemp)
snrReq = 10 #just for now

print(f'Based on the data inputed the Eb/n0 ratio is {snr} dB. The required Eb/n0 ratio is {snrReq} dB') 			#It is assumed that the SNR = Eb/nO, in other words that bitrate = bandwidth noise, don't forget the 3dB margin