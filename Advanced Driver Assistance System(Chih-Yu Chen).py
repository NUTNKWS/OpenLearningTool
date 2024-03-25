# QCI&AI Learning Tools Software

# Supported by
# National Science Technology Council, Taiwan
# AI-FML Agent with Machine Learning Tools for AloT Future Applications
# MOST 109-2622-E-024-001-CC1, MOST 110-2622-E-024-003-CC1, MOST 111-2622-E-024-001, and NSTC 112-2622-E-024-002

# Copyright (c) 2024
# KWS Center/OASE Lab. of NUTN, Taiwan
# Zsystem Technology Co., Taiwan
# Mediawave Intelligent Communication Limited., Taiwan
# All rights reserved.

from gpb import delay
from machine import Pin
import pomaspackage as pomaspkg
import display
import image
import utime

import const

def mymin(v1, v2):
    if v1 > v2:
        return v2
    return v1

def mymax(v1, v2):
    if v1 > v2:
        return v1
    return v2

def get_mean(values):
    n = len(values)
    return sorted(values)[n // 2]

class AILearningPlatform:
    def __init__(self):
        #Step 1: Initialize value and Hardware
        self.myLCD = pomaspkg.LcdModule()
        self.mySpeaker = pomaspkg.SpeakerModule()
        self.myButton = pomaspkg.ButtonModule(self.myLCD)
        self.myLED = pomaspkg.LedModule()
        self.myUltrasound = pomaspkg.UltrasoundModule()
        self.myLightSensor = pomaspkg.LightSensorModule()
        self.myDHT = pomaspkg.DHTModule()

        #ClearLCD, showAI-FML Logo, and play audio
        self.myLCD.Clear_LCD()
        self.myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
        self.mySpeaker.playAudio('aifml_logo.wav')
        
        return
        self.wifi = self.initialize_wifi()
        if self.wifi is None:
            raise ValueError("Wifi failed to initialize")
        self.initialize_mqtt()
        

    def initialize_wifi(self):
        #Step 2: Check Wifi
        self.wifi = pomaspkg.WifiUartRT10(const.UART_PORTNO, 115200, self.myLCD)
        self.wifi.vccReboot()
        self.wifi.sendAT('VER') # read version
        self.wifi.cmdAT()
        WifiConnected = self.wifi.wifiConap(const.WIFI_NAME, const.WIFI_PASSWORD)
        # Check if WIFI connection is success or failure
        if not WifiConnected:
            self.mySpeaker.playAudio('WiFiFailure.mp3')
            return None
    
        self.mySpeaker.playAudio('WiFiConnected.mp3')
        self.wifi.wifiGetip()
        return True
        
    def initialize_mqtt(self):
        #Step 3: Check MQTT Server
        self.wifi.mqttSetup(const.MQTT_USERNAME, const.MQTT_PASSWORD)
        MQTTConnected = self.wifi.mqttCon(const.MQTT_SERVER, const.MQTT_PORTNO, const.MQTT_CLIENTID)
        #Check if MQTT connection is success or failure
        if not MQTTConnected:
            self.mySpeaker.playAudio('MQTTFailure.mp3')
            return False
    
        #Subscribe Topic
        self.wifi.mqttSub(const.MQTT_AIFMLTOPIC, const.MQTT_pqos, const.MQTT_WaitTime)
        delay(1000)
        self.myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
        return True
        
    def ADAS_startLCD(self):
        self.myLCD.ShowMessage_LCD('If you do not have WIFI\n->Click Button 1\nElse\n->Click Button 2')
    
    def getInferenceData(self):
        topic, inference_string = self.wifi.mqttRecv(const.MQTT_CHKRECV_COUNT)
        return inference_string

    def InferenceADAS(topic, inference_string):              
        if(inference_string == ''):
            return
        inference_number = float(inference_string)
        img = image.Image(320, 240, image.RGB565)
        brightness = mymin(int(inference_number), 100)
        scaled_distance = mymin(int(inference_number), 100)
        red_part = int(255 - inference_number)
        green_part = int(inference_number)
        
        if inference_number <= 60:
            #img.draw_circle(160, 120, 100 - mymin(int(inference_number), 100), (red_part * brightness // 255,green_part * brightness // 255,0), fill=True)
            img.draw_circle(160, 120, 100 - mymin(int(inference_number), 100), (255,0,0), fill=True)
            display.set_frame(img)
            img.draw_string(10,10, "You are too close!", (255,255,255),scale=2,monospace=False)
            img.draw_string(10,50, "Watch out!", (255,255,255),scale=2,monospace=False)
            display.set_frame(img)
            delay(10)
            
        elif (inference_number > 60 and inference_number <= 175):
            img.draw_circle(160, 120, 125 - mymin(int(inference_number), 100), (red_part * brightness // 255,green_part * brightness // 255,0), fill=True)
            display.set_frame(img)
            img.draw_string(10,10, "Keep going!", (255,255,255),scale=2,monospace=False)
            display.set_frame(img)
            delay(10)

        elif (inference_number > 175):
            img.draw_circle(160, 120, 110 - mymin(int(inference_number), 100), (red_part * brightness // 255,green_part * brightness // 255,0), fill=True)
            display.set_frame(img)
            img.draw_string(10,10, "It's safe!", (255,255,255),scale=2,monospace=False)
            display.set_frame(img)
            delay(10)
              
    def RealTimeADAS(self):
        k = 10
        distances = [255] * k
        lights = [255] * k
        humidities = [0] * k
        temperatures = [0] * k
        while True:
            # Get new values
            dist = self.myUltrasound.getDistance()
            if dist == 0:
                dist = 255
            distances.append(dist)
            lights.append(self.myLightSensor.getLight())
            humidities.append(float(self.myDHT.getHumidity()))
            temperatures.append(float(self.myDHT.getTemperature()))
               
            # Cleanup old values
            distances.pop(0)
            lights.pop(0)
            humidities.pop(0)
            temperatures.pop(0)
            
            # Get mean
            distance = get_mean(distances)
            light = get_mean(lights)
            humidity = get_mean(humidities)
            temperature = get_mean(temperatures)
            
            print("D",distance, "L",light, "H",humidity, "T",temperature)
            img = image.Image(320, 240, image.RGB565)
            
            brightness = mymin(int(light // 5), 255)
            scaled_distance = mymin(int(distance), 100)
            red_part = 255 - distance
            green_part = distance
            
            img.draw_circle(160, 120, 100 - mymin(int(distance), 100), (red_part * brightness // 255,green_part * brightness // 255,0), fill=True)            
            
            if distance < 10:
                img.draw_string(10,10, "You are too close!", (255,255,255),scale=2,monospace=False)
                img.draw_string(10,50, "Watch out!", (255,255,255),scale=2,monospace=False)
                
            if light < 60:
                img.draw_string(10, 200, "Its too dark to give you a distance",scale=3, monospace=False)
                            
            display.set_frame(img)
            delay(10)
   
if __name__ == "__main__":
    platform = AILearningPlatform()
    
    #Button1->Real time ADAS
    #Button2->Inference data by ZAI-FML platform and Show result on LCD 
    btnGREEN = Pin('C0',Pin.IN)
    btnYELLOW = Pin('C1',Pin.IN)   
    btnList = [btnGREEN, btnYELLOW]
    
    platform.ADAS_startLCD()
    while True:
        if btnList[0].value() == 0:
            platform.RealTimeADAS()
        
        elif btnList[1].value() == 0:
            platform.initialize_wifi()
            platform.initialize_mqtt()
            while True:
                inference_string = platform.getInferenceData()
                platform.InferenceADAS(inference_string) 