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

from sensor import HC_SR04


class UltrasoundModule():
    def __init__(self):
        self.hcsr = HC_SR04('E5', 'E4') #trig is E4 (IO12), Echo is E5 (IO13)
       

    def getDistance(self):
        v = self.hcsr.Ultrasound()
        return v