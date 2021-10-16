import json
import numpy as np
import comms as co

#Input file

with open("input.json", "r") as inputFile:
	scData = json.load(inputFile)

co.fileConv(scData)

#Outputs (have to write a function in comms.py to calculate each of these values)

print("Link Budget Calculator 1.0\n\n")

snrDown = co.linkBudget(scData, "downlink")
snrUp = co.linkBudget(scData, "uplink")
snrReq = co.calcRequiredNoiseRatio(scData["AdditionnalParameters"], scData["Mission"])[0]

print(f'Based on the data inputed the Eb/n0 ratio for downlink is {snrDown:.2f} dB and {snrUp:.2f} dB for uplink. The required Eb/n0 ratio is {snrReq:.2f} dB. This leaves a margin of {snrDown-snrReq:.2f} dB for the downlink and {snrUp-snrReq:.2f} dB for uplink' ) 			#It is assumed that the SNR = Eb/nO, in other words that bitrate = bandwidth noise, don't forget the 3dB margin
print("Note: The margin should be at least 3dB to ensure the robustness of the communication system.")