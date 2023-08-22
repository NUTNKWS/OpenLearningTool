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


import const

def organizeMsg(outv_msg, msg):
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


def Activate_Hardware(outv_msg):
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
    myLED.TurnOff_ledGREEN()
    myLED.TurnOff_ledRED()
          
    #According to the parameters of output fuzzy variable to adjust the boundary of if, elseif, and else
    #print('outv_msg=', outv_msg)
    outv = float(outv_msg)
    lcdMsg = ''
    terminalMsg = ''

    if (outv <= 1.5): 
        #turn off the fan
        mySpeaker.playAudio('fan_no.mp3')
        myFan.Control_Fan(0)
        myLCD.ShowImage_LCD('fan_off.bmp', const.LCDImgDelayTime)
        lcdMsg, terminalMsg = organizeMsg(outv_msg, 'Turn off the fan.')
        #control LED to flash
        myLED.Flash_ledGREENledRED(2, 200)       
           
    elif (outv > 1.5 and outv <= 5.5):       
        #turn on the fan but weakly
        mySpeaker.playAudio('fan_weak.mp3')
        myFan.Control_Fan(400)
        myLCD.ShowImage_LCD('fan_on.bmp', const.LCDImgDelayTime)
        lcdMsg, terminalMsg = organizeMsg(outv_msg, 'Turn on the fan Weakly.')
        myLED.Flash_ledRED(2, 200)
                   
    elif (outv > 5.5):       
        #turn on the fan but strongly
        mySpeaker.playAudio('fan_strong.mp3')
        myFan.Control_Fan(700)
        myLCD.ShowImage_LCD('fan_onstrong.bmp', const.LCDImgDelayTime)
        lcdMsg, terminalMsg = organizeMsg(outv_msg, 'Turn on the fan Strongly.')    
        myLED.Flash_ledGREEN(2, 200)        
           
    

    #show message on LCD
    if (lcdMsg != ''):
        myLCD.ShowMessage_LCD(lcdMsg)

    #show message on terminal
    if (terminalMsg != ''):
        print(terminalMsg)

    #turn off the fan
    myFan.Control_Fan(0) 
    #light off
    myLED.TurnOff_ledGREEN()
    myLED.TurnOff_ledRED()       
           
       

if __name__ == '__main__':
    #Step 1: Initialize value and Hardware
    myLCD = pomaspkg.LcdModule()
    mySpeaker = pomaspkg.SpeakerModule()
    myButton = pomaspkg.ButtonModule(myLCD)
    myLED = pomaspkg.LedModule()
    myFan = pomaspkg.FanModule()

    #ClearLCD, showAI-FML Logo, and play audio
    myLCD.Clear_LCD()
    myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
    mySpeaker.playAudio('aifml_logo.wav')

    #Step 2: Check Wifi
    wifi = pomaspkg.WifiUartRT10(const.UART_PORTNO, 115200, myLCD)
    wifi.vccReboot()
    wifi.sendAT('VER') # read version
    wifi.cmdAT()
    WifiConnected = wifi.wifiConap(const.WIFI_NAME, const.WIFI_PASSWORD)
    #Check if WIFI connection is success or failure
    if (WifiConnected == True):
        mySpeaker.playAudio('WiFiConnected.mp3')
        wifi.wifiGetip()
        #Step 3: Check MQTT Server
        wifi.mqttSetup(const.MQTT_USERNAME, const.MQTT_PASSWORD)
        MQTTConnected = wifi.mqttCon(const.MQTT_SERVER, const.MQTT_PORTNO, const.MQTT_CLIENTID)
        #Check if MQTT connection is success or failure
        if (MQTTConnected == True):
            #Subscribe Topic
            wifi.mqttSub(const.MQTT_AIFMLTOPIC, const.MQTT_pqos, const.MQTT_WaitTime)
            delay(1000)
            myLCD.ShowImage_LCD('aifml_logo.bmp', const.LCDImgDelayTime)
            while True:
                #Check the received message from the subscribed topic of the MQTT Server
                topic, outv_msg = wifi.mqttRecv(const.MQTT_CHKRECV_COUNT)
                if ((topic == const.MQTT_AIFMLTOPIC) and (outv_msg != '')):
                    Activate_Hardware(outv_msg)               

                #delay(1000)
                myLED.Flash_ledGREEN(1, 200)
        else:
            mySpeaker.playAudio('MQTTFailure.mp3')
    else:
        mySpeaker.playAudio('WiFiFailure.mp3')
    
