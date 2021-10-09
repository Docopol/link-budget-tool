import numpy as np

#SI unit converter

def SIConv(parameter):

	if(parameter["Unit"] == "SI"):
		return parameter
	elif(parameter["Unit"] == "deg"):
		parameter["Value"] *= np.PI()/180
		parameter["Unit"] = "SI"
		return parameter
	elif(parameter["Unit"] == "dB"):
		parameter["Value"] = 10**(parameter["Value"]/10)
		parameter["Unit"] = "SI"
		return parameter



