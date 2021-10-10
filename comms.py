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




def calcGain(frequency, diameter, efficiency=1, length=1, typeAnt="unspecified"):

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

def calcAntennaPointingLoss(frequency, diameter, pointingOffset, typeAnt="unspecified", length=None, halfPowerAngle=None):

	if(typeAnt == "parabolic"):
		halfPowerAngle = 21/180*np.pi/(frequency/1e9*diameter)
	elif(typeAnt == "horn"):
		halfPowerAngle = 225/(180*diameter)*(c/frequency)
	elif(typeAnt == "helical"):
		halfPowerAngle = 52/180*np.pi/(np.pi**2*diameter**2*length/(c/frequency)**3)**(1/2)

	antennaLoss = -12*(pointingOffset/halfPowerAngle)**2

	return antennaLoss


