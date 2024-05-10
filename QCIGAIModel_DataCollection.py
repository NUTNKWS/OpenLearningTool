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
import pomaspackage as pomaspkg

import time
import const

class AILearningPlatform:
    def __init__(self):
        #Step 1: Initialize value and Hardware
        self.myLCD = pomaspkg.LcdModule()
        self.mySpeaker = pomaspkg.SpeakerModule()
        self.myButton = pomaspkg.ButtonModule(self.myLCD)
        self.myLED = pomaspkg.LedModule()        
        self.myUltrasound = pomaspkg.UltrasoundModule()
        self.myLightSensor = pomaspkg.LightSensorModule()
        
        #StatisticalAnalysis
        self.mySA = pomaspkg.StatAnalModule()

        #Timer
        self.myTimer = pomaspkg.TimerModule()

        #Step 2: Save Data
        self.filename = './sd/output/' + self.myTimer.get_CurrentTime() + '_QCIGAI.csv'
        self.mySD = pomaspkg.SDModule()
        self.mySD.DeleteFile(self.filename)
        self.mySD.WriteFile(self.filename, ['No,Distance,Light,HEGAIText,HEGAIImage_v1,HEGAIImage_v2,HEGAIImage,Image'], 'w')
        
        #Step 3: ClearLCD, showAI-FML Logo, and play audio
        self.myLCD.Clear_LCD()
        self.myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
        self.mySpeaker.playAudio('aifml_logo.wav')
        

    def set_led1On (self):
        self.myLED.TurnOn_led1()

    def initialize_Image(self):        
        #activate camera
        img = self.myCamera.ShowSnapShot()        
        return img

    def start_DataCollection(self):
        k = 10
        self.distances = [255] * k
        self.lights = [255] * k
        self.countFarDistance = 0
       

        self.myCamera = pomaspkg.CameraModule()
        self.data_index_old = -1
        self.datacount = 0        

        #always collect the data
        while True:
            #initialize image
            self.img = self.initialize_Image()
            distance, light = self.measure_data()            
            print("D", distance, "L", light)

            #show real-time distance and light on the LCD
            data_str = 'D: ' + str(distance) + ' L: ' + str(light) + '\n'
            self.img.draw_string(10, 200, data_str, (255, 0, 0), scale = 2, mono_space = False)
            #show both cirle and message on LCD
            self.myLCD.Show_LCD(self.img, 0)

            #check people take a photo or not
            self.checkTakePhoto(distance, light)
            
            #flash green led                        
            self.myLED.Flash_ledGREEN(1, 200)
            delay(200)

    def measure_data(self):
        '''
        Function: Measure data about distance and light by average
        '''
        # Get new values
        # distance
        dist = self.myUltrasound.getDistance()
        if dist != 0:
            self.distances.append(dist)
            self.distances.pop(0)
            self.countFarDistance = 0
        else:
            #when the distance is too close or too far, dist will be 0. So, we need to filter it.
            self.countFarDistance = self.countFarDistance + 1
            if (self.countFarDistance >= const.ADAS_MaxcountFarDistance):
                '''when dist is 0 for more than const.countFarDistance times, 
                    then it is real too close or too far.
                    For this situation, just set dist to 255.
                '''
                dist = 255
                self.distances.append(dist)
                self.distances.pop(0)
                self.countFarDistance = 0
        #light
        self.lights.append(self.myLightSensor.getLight())       
               
        # Cleanup oldest values for light
        self.lights.pop(0)
        
            
        # Get mean value of distance, light
        distance = self.mySA.get_mean(self.distances)
        light = self.mySA.get_mean(self.lights)
        
        return distance, light

    def checkTakePhoto(self, distance, light):
        '''
        Function: Take a photo to collect the data
        '''
        #check 1st button pressed (1st green button)
        data_index_new = self.myButton.getButtonPressed(self.data_index_old)                                        
        #Save the snapshot image to SD
        if (data_index_new == 0):            
            #yes, play the sound and save the image
            self.mySpeaker.playAudio('takephoto.mp3')            
            #store file
            datacount_str = self.myTimer.timestamp + '_' + str(self.datacount + 1) + '.jpg'
            image_filename = './sd/output/' + datacount_str
            #write time information to the LCD
            self.img.draw_string(10, 220, datacount_str, (255, 0, 0), scale = 2, mono_space = False)
            self.mySD.WriteImage(image_filename, self.img)
            
            #store data
            #csv format: ['No,Distance,Light,GAIText,GAIImage_v1,GAIImage_v2,GAIImage,Image']
            self.mySD.WriteFile(self.filename, [str(self.datacount + 1) + ',' + str(distance) + ',' + str(light)+ ',,,,,' + datacount_str], 'a')
            self.data_index_old = -1
            self.datacount = self.datacount + 1
       
        

if __name__ == '__main__':
    platform = AILearningPlatform()
    platform.set_led1On()
    platform.start_DataCollection()
    
 