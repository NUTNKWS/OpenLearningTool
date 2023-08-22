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

from machine import PWM
from gpb import delay

class FanModule():
    def __init__(self):
        self.fan = PWM(2, 200, 0)
        pwm3 = PWM(3, 200, 0)

    def Control_Fan(self, value):
        self.fan.duty(value)