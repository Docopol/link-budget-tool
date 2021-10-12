import numpy as np

##Main calculation function

def linkBudget(scData, mode):
	
	scPower = SItodB(scData["Spacecraft"]["Power"]["Value"])
	scTransLoss = SItodB(scData["Spacecraft"]["LossFactor"]["Value"])
	gsRecLoss = SItodB(scData["GroundStation"]["LossFactor"]["Value"])

	if(mode == "downlink"):

		scGain = calcGain(scData["Mission"]["FrequencyDownlink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["Antenna"]["Efficiency"]["Value"])
		scPointLoss = calcPointingLoss(scData["Mission"]["FrequencyDownlink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["OffsetPointing"]["Value"], scData["Spacecraft"]["Antenna"]["HalfPowerAngle"]["Value"])
		
		gsGain = calcGain(scData["Mission"]["FrequencyDownlink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["Antenna"]["Efficiency"]["Value"])
		gsPointLoss = calcPointingLoss(scData["Mission"]["FrequencyDownlink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["OffsetPointing"]["Value"], scData["GroundStation"]["Antenna"]["HalfPowerAngle"]["Value"])
		
		systemNoiseTemp = calcSystemNoise(scData["Mission"]["FrequencyDownlink"]["Value"], "downlink")
		transmissionPathLoss = calcTransPathLoss(scData["Mission"]["FrequencyDownlink"]["Value"])
		freeSpaceLoss = calcSpaceLoss(scData["Mission"]["Planet"], scData["Mission"]["FrequencyDownlink"]["Value"], scData["Mission"]["OrbitingBodyRadius"]["Value"], scData["Mission"]["OrbitalHeight"]["Value"], scData["Mission"]["SpacecraftSunDistance"]["Value"], scData["Mission"]["ElongationAngle"]["Value"])

		transmissionDataRate = calcTransmissionDataRate(scData["Payload"], scData["Mission"])

	elif(mode == "uplink"):
		scGain = calcGain(scData["Mission"]["FrequencyUplink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["Antenna"]["Efficiency"]["Value"])
		scPointLoss = calcPointingLoss(scData["Mission"]["FrequencyUplink"]["Value"], scData["Spacecraft"]["Antenna"]["Type"], scData["Spacecraft"]["Antenna"]["Diameter"]["Value"], scData["Spacecraft"]["Antenna"]["Length"]["Value"], scData["Spacecraft"]["OffsetPointing"]["Value"], scData["Spacecraft"]["Antenna"]["HalfPowerAngle"]["Value"])
		
		gsGain = calcGain(scData["Mission"]["FrequencyUplink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["Antenna"]["Efficiency"]["Value"])
		gsPointLoss = calcPointingLoss(scData["Mission"]["FrequencyUplink"]["Value"], scData["GroundStation"]["Antenna"]["Type"], scData["GroundStation"]["Antenna"]["Diameter"]["Value"], scData["GroundStation"]["Antenna"]["Length"]["Value"], scData["GroundStation"]["OffsetPointing"]["Value"], scData["GroundStation"]["Antenna"]["HalfPowerAngle"]["Value"])
		
		systemNoiseTemp = calcSystemNoise(scData["Mission"]["FrequencyUplink"]["Value"], "uplink")
		transmissionPathLoss = calcTransPathLoss(scData["Mission"]["FrequencyUplink"]["Value"])
		freeSpaceLoss = calcSpaceLoss(scData["Mission"]["Planet"], scData["Mission"]["FrequencyUplink"]["Value"], scData["Mission"]["OrbitingBodyRadius"]["Value"], scData["Mission"]["OrbitalHeight"]["Value"], scData["Mission"]["SpacecraftSunDistance"]["Value"], scData["Mission"]["ElongationAngle"]["Value"])

		transmissionDataRate = scData["Mission"]["RequiredUplinkDataRate"]["Value"]

	snr = scPower + scTransLoss + scGain + transmissionPathLoss + gsGain + freeSpaceLoss + scPointLoss + gsPointLoss + gsRecLoss + 228.6 - 10*np.log10(transmissionDataRate) - 10*np.log10(systemNoiseTemp)
	# snr = 0
	return snr	



## Other functions

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
		if(isinstance(value, dict) and (("Value" in value.keys()) and ("Unit" in value.keys()))): 
			SIConv(value)
		elif(isinstance(value, dict)):
			fileConv(value)

def dBtoSI(parameter):
	parameterIndB = 10**(parameter/10)
	return parameterIndB

def SItodB(parameter):
	parameterInSI = 10*np.log10(parameter)
	return parameterInSI

##Losses/gain functions

def calcGain(frequency, typeAnt, diameter, length, efficiency):

	c = 3e8

	if(typeAnt == "unspecified"):
		gain = dBtoSI((np.pi**2*diameter**2)/(c/frequency)**2*efficiency)
	elif(typeAnt == "parabolic"):
		gain = 20*np.log10(diameter)+20*np.log10(frequency/1e9)+17.8
	elif(typeAnt == "horn"):
		gain = 20*np.log10(np.pi*diameter/(c/frequency))-2.8
	elif(typeAnt == "helical"):
		gain = 10*np.log10((np.pi**2*diameter**2*length)/((c/frequency)**3))+10.3

	return gain

def calcPointingLoss(frequency, typeAnt, diameter, length, pointingOffset, halfPowerAngle):

	c = 3e8
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

def calcTransPathLoss(frequency): #valid for frequencies less than 57GHz and elevation angles greater than 10deg
	elevationAngle = 45/180*np.pi
	waterVapourDensity = 1270

	specificAtenuationOxygen = (0.00719+6.09/((frequency/1e9)**2+0.227)+4.81/((frequency/1e9-57)**2+1.5))*(frequency/1e9)**2/(1e3)
	specificAtenuationWater = (0.067+2.4/((frequency/1e9-22.3)**2+6.6)+7.33/((frequency/1e9-183.5)**2+5))*(frequency/1e9)**2*waterVapourDensity/(1e4)

	totalGaseousAtenuation = -(8*specificAtenuationOxygen+2*specificAtenuationWater)/np.sin(elevationAngle)

	return totalGaseousAtenuation

def calcSpaceLoss(missionType, frequency, orbitingBodyRadius, orbitalHeight, scSunDist, elongationAngle):

	c = 3e8

	if(missionType == "Earth"):
		worstCaseDistance = ((orbitingBodyRadius+orbitalHeight)**2-orbitingBodyRadius**2)**(1/2)
	elif(missionType == "Moon"):
		worstCaseDistance = 384399e3
	else:
		earthSunDist = 1.495678e11
		worstCaseDistance = (earthSunDist**2+scSunDist**2-2*earthSunDist*scSunDist*np.cos(elongationAngle))**(1/2)

	spaceLoss = (c/(4*np.pi*worstCaseDistance*frequency))**2
	spaceLossindB = SItodB(spaceLoss)

	return spaceLossindB

def calcDataRateLineImager(swathWidth, pixelSize, bitsPerPixel, scGroundVelocity):
	dataRate = bitsPerPixel*swathWidth*scGroundVelocity/pixelSize**2
	return dataRate

def calcTransmissionDataRate(payloads, mission):

	totalRequiredDataRate = 0

	for payload in payloads.values():
		if(payload["GeneratedDataRate"]["Value"] != 0):
			generatedDataRate = payload["GeneratedDataRate"]["Value"]
		elif(payload.key == "LineImager"):
			generatedDataRate = calcDataRateLineImager(payload["SwathWidth"]["Value"], payload["PixelSize"]["Value"], payload["BitsPerPixel"]["Value"], mission["GroundVelocity"]["Value"])

		requiredDataRate = generatedDataRate*payload["DutyCycle"]["Value"]/mission["DownlinkTimeRatio"]["Value"]

		totalRequiredDataRate += requiredDataRate

	return totalRequiredDataRate