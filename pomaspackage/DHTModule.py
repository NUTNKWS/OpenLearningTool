# AIoT-FML Learning Tools Software

# Supported by
# Ministry of Science and Technology (MOST), Taiwan
# AI-FML Agent with Machine Learning Tools for AloT Future Applications
# MOST 109-2622-E-024-001-CC1, MOST 110-2622-E-024-003-CC1, and MOST 111-2622-E-024-001

# Copyright (c) 2023
# KWS Center/OASE Lab. of NUTN, Taiwan
# Zsystem Technology Co., Taiwan
# Mediawave Intelligent Communication Limited., Taiwan
# All rights reserved.

from sensor import DHT11
class DHTModule():
    def __init__(self):
    	self.dht11 = DHT11('E1')
    
    def getTemperature(self):
    	'''
    	Function: read temperature in ℃
    	'''
    	v = self.dht11.temperature()
    	return v

    def getHumidity(self):
    	'''
    	Function: read humidity in %
    	'''
    	v = self.dht11.humidity()
    	return v