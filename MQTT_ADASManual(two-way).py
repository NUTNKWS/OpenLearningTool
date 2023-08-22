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

#inferred result: 17.619(dangerous), 50(medium), 82.381(safe), 31.124(dangerous), and 40.778(medium)
input_data = [
                ['10', '20'],
                ['28', '967'],
                ['171.3', '149.7'],
                ['14', '1090'],
                ['17', '720']]

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

        #ClearLCD, showAI-FML Logo, and play audio
        self.myLCD.Clear_LCD()
        self.myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
        self.mySpeaker.playAudio('aifml_logo.wav')
        
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


    def Activate_Hardware(self, outv_msg):
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
            #not recommended
            self.mySpeaker.playAudio('warning.mp3')
            self.myFan.Control_Fan(0)
            self.myLCD.ShowImage_LCD('biggest.bmp', const.LCDImgDelayTime)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'You are too close!\nWatch out!')
            #control LED to flash
            self.myLED.Flash_ledRED(30, 40)    
               
        elif (outv > 35 and outv <= 65):       
            #recommended
            self.mySpeaker.playAudio('bibi.mp3')
            self.myLCD.ShowImage_LCD('middle.bmp', const.LCDImgDelayTime)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'medium')
            self.myLED.Flash_ledGREENledRED(30, 40)
                       
        elif (outv > 65):       
            #very recommended
            self.mySpeaker.playAudio('ifeelgood.mp3')
            self.myFan.Control_Fan(700)
            self.myLCD.ShowImage_LCD('smallest.bmp', const.LCDImgDelayTime)
            lcdMsg, terminalMsg = self.organizeMsg(outv_msg, 'safe')
            self.myLED.Flash_ledGREEN(30, 40)        
               

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

    def start(self):
        
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
                self.Activate_Hardware(outv_msg)                 
               
            self.myLED.Flash_ledGREEN(1, 200)

   
if __name__ == "__main__":
    platform = AILearningPlatform()
    platform.start()