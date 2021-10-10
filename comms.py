import numpy as np

#SI unit converter

def SIConv(parameter):
	if(parameter["Unit"] == "SI"):
		return parameter
	elif(parameter["Unit"] == "deg"):
		parameter["Value"] *= np.pi/180
		parameter["Unit"] = "SI"
		return parameter
	elif(parameter["Unit"] == "dB"):
		parameter["Value"] = 10**(parameter["Value"]/10)
		parameter["Unit"] = "SI"
		return parameter

def fileConv(dataName):
	for key, value in dataName.items():
		print(key, value)
		if(isinstance(value, dict) and (("Value" in value.keys()) and ("Unit" in value.keys()))): 
			SIConv(value)
		elif(isinstance(value, dict)):
			fileConv(value)

def dBConv(parameter):
	parameterIndB = 10**(parameter/10)
	return parameterIndB

def calcGain(frequency, typeAnt, diameter, length, efficiency):

	c = 3e8

	if(typeAnt == "unspecified"):
		gain = dBConv((np.pi**2*diameter**2)/(c/frequency)**2*efficiency)
	elif(typeAnt == "parabolic"):
		gain = 20*np.log10(diameter)+20*np.log10(frequency/1e9)+17.8
	elif(typeAnt == "horn"):
		gain = 20*np.log10(np.pi*diameter/(c/frequency))-2.8
	elif(typeAnt == "helical"):
		gain = 10*np.log10((np.pi**2*diameter**2*length)/((c/frequency)**3))+10.3

	return gain

def calcPointingLoss(frequency, typeAnt, diameter, length, pointingOffset, halfPowerAngle):

	if(typeAnt == "parabolic"):
		halfPowerAngle = 21/180*np.pi/(frequency/1e9*diameter)
	elif(typeAnt == "horn"):
		halfPowerAngle = 225/(180*diameter)*(c/frequency)
	elif(typeAnt == "helical"):
		halfPowerAngle = 52/180*np.pi/(np.pi**2*diameter**2*length/(c/frequency)**3)**(1/2)

	antennaLoss = -12*(pointingOffset/halfPowerAngle)**2

	return antennaLoss


def calcSystemNoise(frequency, mode): #values taken from S5 p14
	cableLossNoise = 35

	if(mode == "downlink"):
		if(frequency == 0.2e9):
			antennaNoise = 150
			receiverNoise = 36
		elif(frequency > 2e9 and frequency < 12e9):
			antennaNoise = 25
			receiverNoise = 75
		else:
			antennaNoise = 100
			receiverNoise = 289

	elif(mode == "crosslink"):
		antennaNoise = 20
		receiverNoise = 627
	elif(mode == "uplink"):
		if(frequency > 0.2e9 and frequency < 20e9):
			antennaNoise = 290
			receiverNoise = 289
		elif(frequency == 40e9):
			antennaNoise = 290
			receiverNoise = 438

	totalNoise = antennaNoise+cableLossNoise+receiverNoise

	return totalNoise

# def calcTransPathLoss(frequency):
	