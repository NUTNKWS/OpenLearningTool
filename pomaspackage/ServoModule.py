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

from gpb import Servo
from gpb import delay

class ServoModule():
    def __init__(self):
        #Use PWM8 to control Servo1
    	self.servo = Servo(1) 
        self.ControlServo_stop()

    def ControlServo_clockwise(self, angle):
    	'''
    	Function: Control Servo to rotate in clockwise (<0, negative)
    	'''
    	#stop
        self.servo.angle(0)
        #wait for 500msec      
        delay(500)
        #rotate the servo in direction of clockwise (negative)       
        self.servo.angle(0-angle)
        delay(500)

    def ControlServo_counterclockwise(self, angle):
        '''
        Function: Control Servo to rotate in counterclockwise(>0, postive)
        '''
        #stop
        self.servo.angle(0)
        #wait for 500msec      
        delay(500)
        #rotate the servo in direction of counterclockwise(postive)          
        self.servo.angle(angle)
        delay(500)

    def ControlServo_stop(self):
        #stop
        self.servo.angle(0)
        #wait for 500msec      
        delay(500)