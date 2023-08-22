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

import gpb
from machine import Pin
from gpb import delay

class LedModule():
    def __init__(self):
        #LED
        self.ledRED = Pin('F2', Pin.OUT) #RedLed
        self.ledGREEN = Pin('F3', Pin.OUT) # GreenLed
        self.led0 = Pin('C12', Pin.OUT)
        self.led1 = Pin('C13', Pin.OUT)
        self.led2 = Pin('C14', Pin.OUT)
        self.led3 = Pin('C15', Pin.OUT)
        
        self.Big_ledList = [self.ledRED, self.ledGREEN]
        self.Small_ledList = [self.led0, self.led1, self.led2, self.led3]

        #turn off all of the leds
        self.TurnOff_allLed(self.Big_ledList)
        self.TurnOff_allLed(self.Small_ledList)

    def TurnOn_led0(self):
        self.led0.on()
    
    def TurnOff_led0(self):
        self.led0.off()
    
    def TurnOn_led1(self):
        self.led1.on()
        
    def TurnOff_led1(self):
        self.led1.off()

    def Toggle_Small_led(self):
        #0 to 1, and 1 to 0 for all smallLed
        for i in range(len(self.Small_ledList)):
            gpb.LED(i).toggle()
        
    def TurnOff_allLed(self, ledList):
        # on() is turn on the light, off() is turn off the light
        for led in ledList:
            led.off()

    def TurnOn_allLed(self, ledList):
        # on() is turn on the light, off() is turn off the light
        for led in ledList:
            led.on()

    def TurnOff_ledGREEN(self):
        self.ledGREEN.off()

    def TurnOff_ledRED(self):
        self.ledRED.off()

    def TurnOn_Led(self, led):
        led.on()

    def TurnOff_Led(self, led):
        led.off()

    def Flash_ledGREENledRED(self, count, delaytime):    
        for i in range(count):
            self.TurnOn_Led(self.ledGREEN)
            self.TurnOn_Led(self.ledRED)
            delay(delaytime)
            self.TurnOff_Led(self.ledGREEN)
            self.TurnOff_Led(self.ledRED) 
            delay(delaytime)       

    def Flash_ledRED(self, count, delaytime):   
        for i in range(count):            
            self.TurnOn_Led(self.ledRED)
            delay(delaytime)      
            self.TurnOff_Led(self.ledRED)
            delay(delaytime)

    def Flash_ledGREEN(self, count, delaytime):   
        for i in range(count):            
            self.TurnOn_Led(self.ledGREEN)
            delay(delaytime)      
            self.TurnOff_Led(self.ledGREEN)
            delay(delaytime)

    def Flash_ledGREENledREDONOFF(self, count, delaytime):   
        for i in range(count):     
            self.TurnOn_Led(self.ledGREEN)
            self.TurnOff_Led(self.ledRED)
            delay(delaytime)
            self.TurnOff_Led(self.ledGREEN)
            self.TurnOn_Led(self.ledRED)
            delay(delaytime)

    def Flash_ledRED(self, count, delaytime):
        for i in range(count):            
            self.TurnOn_Led(self.ledRED)
            delay(delaytime)      
            self.TurnOff_Led(self.ledRED)
            delay(delaytime)

    def Flash_ledGREEN(self, count, delaytime):
        for i in range(count):            
            self.TurnOn_Led(self.ledGREEN)
            delay(delaytime)      
            self.TurnOff_Led(self.ledGREEN)
            delay(delaytime)

