import json
import numpy as np
import comms as co

#Input file

with open("input.json", "r") as inputFile:
	scData = json.load(inputFile)

#Inputs

scPower = co.SIConv(scData["Spacecraft"]["Power"])
scTransLoss = co.SIConv(scData["Spacecraft"]["LossFactor"])
gsRecLoss = co.SIConv(scData["GroundStation"]["LossFactor"])
scSignalFrequency = co.SIConv(scData["Spacecraft"]["Frequency"])

#Outputs (have to write a function in comms.py to calculate each of these values)

scGain = 10
transmissionPathLoss = -10
gsGain = 100
freeSpaceLoss = -10
scAntennaPointLoss = -10
dataRate = 10
systemNoiseTemp = 10


# snr = scPower + scTransmitterLoss + scGain + transmissionPathLoss + gsGain + freeSpaceLoss + antennaPointLoss + gsRecLoss + 228.6 - 10*np.log(dataRate) - 10*np.log(systemNoiseTemp)
# snrReq = 10 #just for now

# print(f'Based on the data inputed the Eb/n0 ratio is {snr} dB. The required Eb/n0 ratio is {snrReq} dB') 			#It is assumed that the SNR = Eb/nO, in other words that bitrate = bandwidth noise, don't forget the 3dB margin