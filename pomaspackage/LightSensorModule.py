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

from machine import ADC     
from gpb import delay            


class LightSensorModule():
    def __init__(self):
        #create the source of the light
        self.light = ADC(2)
        self.light_threshold = self.setLightThreshold()
    
    
    def setLightThreshold(self):
        light_threshold = 0               
        for i in range(30):              
            light_threshold = light_threshold + self.getLight()
            delay(20)
            light_threshold = light_threshold / 30 + 200
        return light_threshold


    def getLight(self):
    	'''
    	Function: read light
    	'''
    	v = self.light.read()
    	return v
