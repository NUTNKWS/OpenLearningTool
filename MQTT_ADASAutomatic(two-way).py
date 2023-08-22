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
import display
import image
import utime


import const

#inferred result: 17.619(dangerous), 50(medium), 82.381(safe), 31.124(dangerous), and 40.778(medium)
input_data = [['20', '30'],
                ['100', '120'],
                ['200', '200'],
                ['100', '120'],
                ['200', '200']]

class AILearningPlatform:
    def __init__(self):
        #Step 1: Initialize value and Hardware
        self.myLCD = pomaspkg.LcdModule()
        self.mySpeaker = pomaspkg.SpeakerModule()
        self.myButton = pomaspkg.ButtonModule(self.myLCD)
        self.myLED = pomaspkg.LedModule()
        self.myFan = pomaspkg.FanModule()
        self.myUltrasound = pomaspkg.UltrasoundModule()
        self.myLightSensor = pomaspkg.LightSensorModule()
        self.myDHT = pomaspkg.DHTModule()

        #SD
        self.filename = './sd/output/ADAS.csv'
        self.mySD = pomaspkg.SDModule()
        self.mySD.DeleteFile(self.filename)
        #write the name of the column
        self.mySD.WriteFile(self.filename, ['Distance,Light,Humidity,Temperature'], 'a')

        #ClearLCD, showAI-FML Logo, and play audio
        self.myLCD.Clear_LCD()
        self.myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
        self.mySpeaker.playAudio('aifml_logo.wav')

        #StatisticalAnalysis
        self.mySA = pomaspkg.StatAnalModule()
        
        #check Wifi and MQTT
        self.wifi = self.initialize_wifi()
        if self.wifi is None:
            raise ValueError("Wifi failed to initialize")
        else:
            self.MQTT = self.initialize_mqtt()
            
        

    def initialize_wifi(self):
        #Step 2: Check Wifi
        wifi = pomaspkg.WifiUartRT10(const.UART_PORTNO, 115200, self.myLCD)
        wifi.vccReboot()
        wifi.sendAT('VER') # read version
        wifi.cmdAT()
        WifiConnected = wifi.wifiConap(const.WIFI_NAME, const.WIFI_PASSWORD)
        # Check if WIFI connection is success or failure
        if not WifiConnected:
            self.mySpeaker.playAudio('WiFiFailure.mp3')
            return None
    
        self.mySpeaker.playAudio('WiFiConnected.mp3')
        wifi.wifiGetip()
        return wifi
    
    def initialize_mqtt(self):
        #Step 3: Check MQTT Server
        self.wifi.mqttSetup(const.MQTT_USERNAME, const.MQTT_PASSWORD)
        MQTTConnected = self.wifi.mqttCon(const.MQTT_SERVER, const.MQTT_PORTNO, const.MQTT_CLIENTID)
        #Check if MQTT connection is success or failure
        if not MQTTConnected:
            self.mySpeaker.playAudio('MQTTFailure.mp3')
            return False
    
        #Subscribe Topic
        self.wifi.mqttSub(const.MQTT_AIFMLTOPIC_Subscriber, const.MQTT_pqos, const.MQTT_WaitTime)
        delay(1000)
        self.myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
        return True
    
    def organizeMsg(self, outv_msg, msg):
        '''
        Function: Organize the msg to show it on the LCD
        Input:
        (1) msg: inferred result
        (2) data: input data
        Output: message which shows on the LCD and terminal
        '''
        outv = float(outv_msg)
        #show value with 3 decimal
        lcdMsg = 'ZAI-FML: {:.3f}'.format(outv) + '\r\n{}'.format(msg)
        terminalMsg = 'ZAI-FML: {:.3f}'.format(outv) + ' ({})'.format(msg)
        return lcdMsg, terminalMsg


    def Automatic_Activate_Hardware(self, outv_msg, img):
        '''
            Function: Activate Hardware according to outv, and show message on LCD and terminal
            Input:
            (1) outv: inferred result
            (2) display: LCD
            (3) lcdMsg: message displayed on LCD
            (4) terminalMsg: message displayed on terminal
        '''
        if (outv_msg == ''):
            #if it is an empty string, end the function
            return
        #light off
        self.myLED.TurnOff_ledGREEN()
        self.myLED.TurnOff_ledRED()
              
        #According to the parameters of output fuzzy variable to adjust the boundary of if, elseif, and else
        #print('outv_msg=', outv_msg)
        outv = float(outv_msg)
        lcdMsg = ''
        terminalMsg = ''

        if (outv <= 35): 
            #safe
            self.mySpeaker.playAudio('safe.wav')
            self.myFan.Control_Fan(300)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'It is safe!')
            img.draw_string(const.LCDStartX, const.LCDStartY, lcdMsg, (0, 255, 0), scale = 3, mono_space = False)
            #control LED to flash
            self.myLED.Flash_ledGREEN(6, 40) 
                
               
        elif (outv > 35 and outv <= 65):       
            #normal
            self.mySpeaker.playAudio('alittlesafe.mp3')
            self.myFan.Control_Fan(0)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'Keep going!')
            img.draw_string(const.LCDStartX, const.LCDStartY, lcdMsg, (255, 88, 10), scale = 3, mono_space = False)
            self.myLED.Flash_ledGREENledRED(15, 40)
                       
        elif (outv > 65):       
            #dangerous
            self.mySpeaker.playAudio('dangerous.mp3')
            self.myFan.Control_Fan(0)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'Dangerous!!!')
            img.draw_string(const.LCDStartX, const.LCDStartY, lcdMsg, (255, 0, 0), scale = 3, mono_space = False)
            self.myLED.Flash_ledRED(30, 40)       
               

        #show message on LCD
        if (lcdMsg != ''):
            self.myLCD.Show_LCD(img, const.LCDImgDelayTime)

        #show message on terminal
        if (terminalMsg != ''):
            print(terminalMsg)

        #light off
        self.myLED.TurnOff_ledGREEN()
        self.myLED.TurnOff_ledRED()        
           
    
    def Manual_Activate_Hardware(self, outv_msg):
        '''
            Function: Activate Hardware according to outv, and show message on LCD and terminal
            Input:
            (1) outv: inferred result
            (2) display: LCD
            (3) lcdMsg: message displayed on LCD
            (4) terminalMsg: message displayed on terminal
        '''
        if (outv_msg == ''):
            #if it is an empty string, end the function
            return
        #light off
        self.myLED.TurnOff_ledGREEN()
        self.myLED.TurnOff_ledRED()
              
        #According to the parameters of output fuzzy variable to adjust the boundary of if, elseif, and else
        #print('outv_msg=', outv_msg)
        outv = float(outv_msg)
        lcdMsg = ''
        terminalMsg = ''

        if (outv <= 35): 
            #safe
            self.mySpeaker.playAudio('ifeelgood.mp3')
            self.myFan.Control_Fan(300)
            self.myLCD.ShowImage_LCD('smallest.bmp', const.LCDImgDelayTime)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'It is safe!')
            #control LED to flash
            self.myLED.Flash_ledGREEN(30, 40)    
               
        elif (outv > 35 and outv <= 65):       
            #normal
            self.mySpeaker.playAudio('bibi.mp3')
            self.myFan.Control_Fan(0)
            self.myLCD.ShowImage_LCD('middle.bmp', const.LCDImgDelayTime)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'Keep going!')
            self.myLED.Flash_ledGREENledRED(30, 40)
                       
        elif (outv > 65):       
            #dangerous
            self.mySpeaker.playAudio('warning.mp3')
            self.myFan.Control_Fan(0)
            self.myLCD.ShowImage_LCD('biggest.bmp', const.LCDImgDelayTime)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'Dangerous!!!')
            self.myLED.Flash_ledRED(30, 40)                                   

        #show message on LCD
        if (lcdMsg != ''):
            self.myLCD.ShowMessage_LCD(lcdMsg)

        #show message on terminal
        if (terminalMsg != ''):
            print(terminalMsg)

        
        self.myFan.Control_Fan(0)

        #light off
        self.myLED.TurnOff_ledGREEN()
        self.myLED.TurnOff_ledRED()        

    def getInputData(self, index):
        '''
        Function: read input data according to index
        Output: data that will be sent and use 'underline(_)' to connect the input data
        '''    
        data = input_data[index]
        data_str = const.MQTT_Publish_Separator.join(data)
        return data_str

    def set_led1On (self):
        self.myLED.TurnOn_led1()


    def start_Manual(self):
        
        if self.MQTT == False:
            return
        
        data_index_old = -1
        while True:
            
            #check button pressed
            data_index_new = self.myButton.getButtonPressed(data_index_old)                                        
            #publish the input_msg to AI-FML
            if (data_index_new >= 0):
                #read data based on data_index
                input_msg = self.getInputData(data_index_new)    
                self.wifi.mqttPub(const.MQTT_pqos, const.MQTT_retain, const.MQTT_AIFMLTOPIC_Publisher, input_msg)
                data_index_old = -1
                   
                
            #Check the received message from the subscribed topic of the MQTT Server
            topic, outv_msg = self.wifi.mqttRecv(const.MQTT_CHKRECV_COUNT)
            #if topic and outv_msg are both correct, then process data
            if ((topic == const.MQTT_AIFMLTOPIC_Subscriber) and (outv_msg != '') and (outv_msg.find(const.MQTT_Publish_Separator) == -1)):
                self.Manual_Activate_Hardware(outv_msg)                 
               
            self.myLED.Flash_ledGREEN(1, 200)

    def initialize_Image(self):
        if (const.ADAS_Camera):
            #activate camera
            img = self.myCamera.ShowSnapShot()
        else:
            #deactivate camera
            img = image.Image(320, 240, image.RGB565)
        return img


    def Check_Save_Photo(self, img):
        '''
        Function: Check if 1st button is pressed. If yes, take a photo.
        Input: img (image)
        '''
        if (const.ADAS_Camera):
            data_index_new = self.myButton.getButtonPressed(self.data_index_old)                                        
            #Save the snapshot image to SD
            if (data_index_new == 0):
                #yes, save the photo
                self.mySpeaker.playAudio('takephoto.mp3')
                self.mySD.WriteImage('./sd/output/photo.jpg', img)
                self.data_index_old = -1
    
    def start_Automatic(self):
        k = 10
        distances = [255] * k
        lights = [255] * k
        humidities = [0] * k
        temperatures = [0] * k
        
        self.countTimer = 0
        self.myCamera = pomaspkg.CameraModule()
        
        self.countFarDistance = 0
        self.data_index_old = -1
        
        while True:
            
            #initialize image
            img = self.initialize_Image()

            #It needs to call delay to activate timer
            self.countTimer = self.countTimer + 1

            # Get new values
            # distance
            dist = self.myUltrasound.getDistance()
            if dist != 0:
                distances.append(dist)
                distances.pop(0)
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
                    distances.append(dist)
                    distances.pop(0)
                    self.countFarDistance = 0
            #light
            lights.append(self.myLightSensor.getLight())
            #humidity
            humidities.append(float(self.myDHT.getHumidity()))
            #temperature
            temperatures.append(float(self.myDHT.getTemperature()))
               
            # Cleanup oldest values for light, humidity, and temperature
            lights.pop(0)
            humidities.pop(0)
            temperatures.pop(0)
            
            # Get mean value of distance, light, humidity, and temperature
            distance = self.mySA.get_mean(distances)
            light = self.mySA.get_mean(lights)
            humidity = self.mySA.get_mean(humidities)
            temperature = self.mySA.get_mean(temperatures)
            
            print("D", distance, "L", light, "H", humidity, "T", temperature)
            
            brightness = self.mySA.mymin(int(light // 5), 255)
            scaled_distance = self.mySA.mymin(int(distance), 100)
            red_part = 255 - int(distance)
            green_part = int(distance)
            
            #print(scaled_distance, red_part, green_part)
            #draw a circle
            img.draw_circle(160, 120, 100 - self.mySA.mymin(int(distance), 100), (red_part * brightness // 255,green_part * brightness // 255,0), fill=True)
            
            #show string
            if distance < 10:
                #alarm so using red color
                img.draw_string(10, 10, "You are too close!", (255, 0, 0), scale = 2, mono_space=False)
                img.draw_string(10, 40, "Watch out!", (255, 0, 0), scale = 2, mono_space=False)
                
            if light < 60:
                #alarm so using red color
                img.draw_string(10, 150, "It is too dark to give a distance.", (255, 0, 0), scale = 2, mono_space=False)
            
            #show D and L using green color
            data_str = 'D: ' + str(distance) + ' L: ' + str(light) + '\n' + 'H: ' + str(humidity) + ' T: ' + str(temperature) + '\n'
            img.draw_string(10, 200, data_str, (0, 255, 0), scale = 2, mono_space = False)
            #show both cirle and message on LCD
            self.myLCD.Show_LCD(img, 0)
            
            #store data
            self.mySD.WriteFile(self.filename, [str(distance) + ',' + str(light)+ ',' + str(humidity)+ ',' + str(temperature)], 'a')
            
            #compose input data string and publish data to MQTT_Service
            if (self.countTimer >= const.MQTT_Publish_Count):
                data_str = str(distance) + const.MQTT_Publish_Separator + str(light)
                self.wifi.mqttPub(const.MQTT_pqos, const.MQTT_retain, const.MQTT_AIFMLTOPIC_Publisher, data_str)
                self.countTimer = 0
            
            #Check the received message from the subscribed topic of the MQTT Server
            topic, outv_msg = self.wifi.mqttRecv(const.MQTT_CHKRECV_COUNT)
            #if topic and outv_msg are both correct, then process data
            if ((topic == const.MQTT_AIFMLTOPIC_Subscriber) and (outv_msg != '') and (outv_msg.find(const.MQTT_Publish_Separator) == -1)):
                self.Automatic_Activate_Hardware(outv_msg, img)
                self.countTimer = 0
               
            #check if press 1st button to save photo
            self.Check_Save_Photo(img)
            
            self.myLED.Flash_ledGREEN(1, 100)
       

if __name__ == "__main__":
    platform = AILearningPlatform()
    if const.ADAS_Automatic:
        platform.set_led1On()
        platform.start_Automatic()
    else:
        platform.start_Manual()
    