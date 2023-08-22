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

from gpb import delay
import pomaspackage as pomaspkg

import time


import const

if __name__ == '__main__':
    #Step 1: Initialize value and Hardware
    myLCD = pomaspkg.LcdModule()
    mySpeaker = pomaspkg.SpeakerModule()
    myLED = pomaspkg.LedModule()
    myDHT = pomaspkg.DHTModule()
    myLightSesnor = pomaspkg.LightSensorModule()
    myUltrasound = pomaspkg.UltrasoundModule()
    mySD = pomaspkg.SDModule()

    #ClearLCD, showAI-FML Logo, and play audio
    myLCD.Clear_LCD()
    myLCD.ShowImage_LCD('aifml_logo.bmp', 500)
    mySpeaker.playAudio('aifml_logo.wav')

    #store file
    filename = './sd/output/data.csv'
    mySD.DeleteFile(filename)
    mySD.WriteFile(filename, ['Distance,Light,Humidity,Temperature'], 'a')

    while True:
        msg = ''
        
        distance = myUltrasound.getDistance()
        light = myLightSesnor.getLight()
        humidity = myDHT.getHumidity()
        temperature = myDHT.getTemperature()

        msg = 'Distance: {}'.format(distance) + ' (cm)\r\n'
        msg = msg + 'Light: {}'.format(light) + '\r\n'
        msg = msg + 'Humidity : {}'.format(humidity) + ' (%)\r\n'
        msg = msg + 'Temperature: {}'.format(temperature) +' (C)\r\n'
        myLCD.ShowMessage_LCD(msg)
        print(msg)
        
        #store data
        mySD.WriteFile(filename, [str(distance) + ',' + str(light)+ ',' + str(humidity)+ ',' + str(temperature)], 'a')
            
        myLED.Flash_ledGREEN(1, 200)
        delay(200)