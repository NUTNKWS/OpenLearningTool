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

from gpb import UART, delay
from machine import bytes2str, Pin
import const


class WifiUartRT10():  # 適用模組 MW-RT10BX
    EN_PIN = const.EN_PIN
    
    def __init__(self, uart_ch, bard_rate, lcd): # 用途:將WIFI模組初始化
        self.en = Pin(self.EN_PIN, Pin.OUT)
        self.en.value(0)
        self.uart = UART(uart_ch, bard_rate)
        self.lcd = lcd
        delay(100)
        self.en.value(1)
        delay(500)
        self.uart.uart_write('AT+REB\r\n')  # 重啟 WIFI module 
        delay(100)
        mode_response = self.uart.uart_read(10)
#         print(mode_response)
        print('WIFI module initial success.')
        self.lcd.ShowMessage_LCD('WIFI module initial\r\nsuccess.')

        
    def vccReboot(self):
        self.en.value(0)
        delay(100)
        self.en.value(1)
        delay(500)
        mode_response = self.uart.uart_read(50)
        print('VCC reboot done.')
        
        
    def sendAT(self,a_cmd):
        # 用途:寫入AT command
        self.uart.uart_write('AT+'+ a_cmd +'\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(30))
        print(mode_response, end='')
        
    def cmdAT(self):
        # 用途:確認UART是否正常通訊
        self.uart.uart_write('AT\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(30))
        print(mode_response, end='')
    
    def wifiMode(self,flash,mode):
        # 用途:設置wifi模式([flash:0:不儲存於flash/1:儲存於flash][mode:0:none/1:station/2:softAP/3:station+softAP])
        self.uart.uart_write('AT+WMODE='+ flash + ',' + mode +'\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(30)).strip('\0')
        if mode_response == 'WMODE:OK\r\n':
            print('pass!')
        
    def wifiState(self):
        # 用途:查詢wifi連線狀態(0:未進行連線/1:已連上AP/2:正在進行連線中/3:斷開狀態)
        self.uart.uart_write('AT+WSTATE=?\r\n')
        delay(150)
        mode_response = bytes2str(self.uart.uart_read(10))
        if mode_response == 'WSTATE:0\r\n':
            print('WIFI Not Connected!')
        elif mode_response == 'WSTATE:1\r\n':
            WifiConnected = True
            print('WIFI Connected!')
        elif mode_response == 'WSTATE:2\r\n':
            print('Wifi Connecting...')
        elif mode_response == 'WSTATE:3\r\n':
            print('WIFI Disconnected!')
        elif mode_response == 'WSTATE:4\r\n':
            print('WIFI Disconnected!')
       
            
    def wifiConap(self,ap_ssid,ap_pwd):
        '''
        Function: 連線至AP([ssid:ap名稱][pwd:ap密碼])
        Input:
        (1) ap_ssid: wifi name
        (2) ap_pwd: wifi password
        Output:
        WifiConnected: True: Success, False: Failure
        '''
        WifiConnected = False
        delay(100)
        print('-----Set Station Mode-----')
        self.uart.uart_write('AT+WMODE=0,1\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(30)).strip('\0')
        if mode_response == 'WMODE:OK\r\n':
            print('Station Mode Set Up Completed!')
            self.lcd.ShowMessage_LCD('Station Mode\r\nSet Up Completed!')
        
        print('-----Connecting to Router-----')
        self.lcd.ShowMessage_LCD('Connecting to WIFI\r\nPls wait...')

        self.uart.uart_write('AT+WCAP=' + ap_ssid + ',' + ap_pwd +'\r\n')
        rd_buf = []
        timeout_count = 10000
        while True:
            mode_response = bytes2str(self.uart.uart_read(1))
            if mode_response == '\0':
                pass
            else:
                if mode_response == '\n':
                    response_ = ''.join(rd_buf)    # 將bytes list(rd_buf) 轉成 string
                    if response_ == 'WCAP:OK\r':
                        timeout_count = 10000
                    elif response_ =='WIFI-MSG:CONNECTING\r':
                        timeout_count = 10000
                    elif response_ =='WIFI-MSG:CONNECTED\r':
                        print('WIFI Connected!')
                        self.lcd.ShowMessage_LCD('WIFI Connected!')
                        WifiConnected = True
                        break
                    elif response_ =='WIFI-MSG:CONNECT_FAIL\r':
                        print('WIFI Connection Failure!')
                        self.lcd.ShowMessage_LCD('WIFI Connection Failure!')
                        break
                    rd_buf = []   # rd_buf 清除
                else:
                    rd_buf.append(mode_response)  # 將bytes填到array最後一筆資料
                    
            if timeout_count == 0: # timeout 10s
                print('No Response...Timeout')
                self.lcd.ShowMessage_LCD('No Response..Timeout')
                break
            elif timeout_count == 2000:
                self.uart.uart_write('AT+WCAP=' + ap_ssid + ',' + ap_pwd +'\r\n') # retry 1
                print('RETRY...Connecting')
                self.lcd.ShowMessage_LCD('RETRY..Connecting')
                timeout_count = timeout_count-1
            else:
                timeout_count = timeout_count-1
            delay(1)

        return WifiConnected
        
    
    def wifiGetip(self):
        # 用途:讀取當前AP的IP位置
        self.uart.uart_write('AT+WGIP\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(2))
        if mode_response == 'WG':
            mode_response = bytes2str(self.uart.uart_read(50)).strip('\0')
            print(mode_response)
            
        
    def wifiDiscon(self):
        # 用途:斷開與AP的連線
        self.uart.uart_write('AT+WQAP\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(50)).strip('\0')
        if mode_response == 'WQAP:OK\r\nWIFI-MSG:DISCONNECTED\r\n':
            print('WIFI Disconnected!')
            self.lcd.ShowMessage_LCD('WIFI Disconnected!')
        else:
            print('WIFI Disconnect Error!')
            self.lcd.ShowMessage_LCD('WIFI Disconnect Error!')
                    
    def mqttSetup(self,uname,upwd):
        # 用途:設定MQTT預使用的username跟password
        self.uart.uart_write('AT+MQTTUAP='+ uname + ',' + upwd +'\r\n')
        delay(100)
        mode_response = bytes2str(self.uart.uart_read(30)).strip('\0')
        if mode_response == 'MQTTUAP:OK\r\n':
            print('MQTT username/password set up completed!')
            self.lcd.ShowMessage_LCD('MQTT username and password\r\nset up completed!')
            
    def mqttCon(self,host,port,clientID):
        '''
        Function: Connect to MQTT Server
        Input:
        (1) host: MQTT Server URL or IP
        (2) port: MQTT Server Port Number
        (3) clientID: MQTT clientID
        '''
        MQTTConnected = False
        print('-----MQTT Connecting-----')
        self.lcd.ShowMessage_LCD('Connecting to MQTT\r\n Pls wait...')
        self.uart.uart_write('AT+MQTTCONN='+ host+ ','+ port+ ','+ clientID+'\r\n')
        rd_buf = []
        timeout_count = 10000
        while True:
            mode_response = bytes2str(self.uart.uart_read(1))
            if mode_response == '\0':
                pass
            else:
                if mode_response == '\n':
                    response_ = ''.join(rd_buf)    # 將bytes list(rd_buf) 轉成 string
                    if response_ == 'MQTTCONN:OK\r':
                        timeout_count = 10000
                    elif response_ =='MQTT-MSG:CONNECTING\r':
                        timeout_count = 10000
                    elif response_ =='MQTT-MSG:CONNECTED\r':
                        print('MQTT Connected!')
                        self.lcd.ShowMessage_LCD('MQTT Connected!')
                        MQTTConnected = True
                        break
                    elif response_ =='MQTT-MSG:CONNECT_FAIL\r':
                        print('MQTT Connection Failure!')
                        self.lcd.ShowMessage_LCD('MQTT Connection\r\nFailure!')
                        break
                    rd_buf = []   # rd_buf 清除
                else:
                    rd_buf.append(mode_response)
            if timeout_count == 0: # timeout 10s
                print('MQTT No Response..Timeout')
                self.lcd.ShowMessage_LCD('MQTT No Response\r\nTimeout')
                break
            elif timeout_count == 2000:
                self.uart.uart_write('AT+MQTTCONN='+ host+ ','+ port+ ','+ clientID+'\r\n')
                print('RETRY...MQTT Connecting')
                self.lcd.ShowMessage_LCD('RETRY\r\nMQTT Connecting')
                timeout_count = timeout_count-1
            else:
                timeout_count = timeout_count-1
            delay(1)

        return MQTTConnected
            
    def mqttSub(self, topic, s_qos, s_delay):        
        '''
        Function: Subscribe a specific topic
        '''
        self.uart.uart_write('AT+MQTTSUB='+ topic+ ','+ s_qos+'\r\n')
        delay(s_delay)
        mode_response = bytes2str(self.uart.uart_read(30)).strip('\0')
#         mode_response = self.uart.uart_read(100)
#         print(mode_response)
        if mode_response == 'MQTTSUB:OK\r\n':
            print('MQTT Topic Already Subscribed : ' + topic)
            self.lcd.ShowMessage_LCD('MQTT Topic: ' + topic + '\r\nSubscribed Successfully!')
#             print('Topic:'+topic)
        else:
            print('MQTT Topic Subscription Failed!')
            self.lcd.ShowMessage_LCD('MQTT Topic Subscription\r\nFailed!')
    
    def mqttPub(self,p_qos,retain,topic,data):
        '''
        Function: Publish data (a string) to the specific topic
        '''
        self.uart.uart_write('AT+MQTTPUB='+ p_qos+ ','+ retain+ ','+ topic+ ','+ data+ '\r\n')
        rd_buf = []
        timeout_count = 10000
        while True:
            mode_response = bytes2str(self.uart.uart_read(1))
            if mode_response == '\0':
                pass
            else:
                if mode_response == '\n':
                    response_ = ''.join(rd_buf)    # 將bytes list(rd_buf) 轉成 string
#                     if response_ == 'MQTT-MSG:'+ topic+ ','+ data+ '\r':
#                         timeout_count = 10000
#                     elif response_ =='MQTTPUB:OK\r':
                    if response_ =='MQTTPUB:OK\r':
                        print('MQTT Data (' + data + ') Pushed to (' + topic + ') Successfully!')
                        break
                    elif response_ =='MQTTPUB:ERROR\r':
                        print('MQTT Data push failed!')
                        break
                    rd_buf = []   # rd_buf 清除
                else:
                    rd_buf.append(mode_response)
            if timeout_count == 0: # timeout 10s
                print('Data Push No Response..Timeout')
                break
            elif timeout_count == 5000: # retry 10s
                self.uart.uart_write('AT+MQTTPUB='+ p_qos+ ','+ retain+ ','+ topic+ ','+ data+ '\r\n')
                print('RETRY..Data Sending')
                timeout_count = timeout_count-1
            else:
                timeout_count = timeout_count-1
            delay(1)
            
    def mqttDiscon(self,d_delay):
        # 用途:從MQTT Server斷線
        self.uart.uart_write('AT+MQTTDISC\r\n')
        delay(d_delay)
        mode_response = bytes2str(self.uart.uart_read(50)).strip('\0')
#         mode_response = self.uart.uart_read(100)
#         print(mode_response)
        if mode_response == 'MQTTDISC:OK\r\nMQTT-MSG:DISCONNECTED\r\n':
            print('MQTT Disconnected!')
        else:
            print('MQTT Disconnect Failed!')
    
    def mqttLastwill(self,l_qos,retain,topic,message,l_delay):
        # 用途:向MQTT Server訂閱的某個Topic發送遺囑消息(客戶端段線會傳訊息至Server端)
        self.uart.uart_write('AT+MQTTLWT='+ l_qos+ ','+ retain+ ','+ topic+ ','+ message+ '\r\n')
        delay(l_delay)
        mode_response = bytes2str(self.uart.uart_read(100)).strip('\0')
#         mode_response = self.uart.uart_read(100)
#         print(mode_response)
        if mode_response == 'MQTTLWT:OK\r\n':
            print('Made a Will on MQTT Server!')
    
    def mqttRecv(self, count):
        '''
        Function: Receive message from the subscribed topic
        Output: Recevied topic and message
        '''
        mode_response = ''
        response = ''
        timeout_count = count
        msg = ''
        topic = ''
        while True:
            mode_response = bytes2str(self.uart.uart_read(9))
            if mode_response == 'MQTT-MSG:':
                mode_response = bytes2str(self.uart.uart_read(100)).strip('\0')
                if mode_response != '':
                    #print ('mode_response=', mode_response)
                    response = mode_response.split(',')
                    print ('response=', response)
                    #get received topic
                    topic = response[0]
                    #get received message
                    msg = self.checkLFCR(response[len(response) - 1])                    
                    return topic, msg
            if timeout_count == 0:
                return topic, msg
            else:
                timeout_count = timeout_count-1
            delay(1000)
#         b'MQTT-MSG:pop,444\r\n'
        return topic, msg

    def checkLFCR(self, msg):
        '''
        Function: Check if msg includes LFCR characters
        Input: received msg from the subscribed topic
        Output: return the desired msg
        '''
        #print('msg=', msg)
        LFCRList = ['\r\n', '\r', '\n']
        for lfcr in LFCRList:
            index = msg.find(lfcr)
            if (index != -1):
                #print('index={}'.format(index) + ' msg[:index] = {}'.format(msg[:index]))
                rc_str = msg[:index]
                #replace \x001, \x002, \x00 with ''
                rc = rc_str.replace('\x001','').replace('\x002','').replace('\x00','')
                return rc
        return ''

        