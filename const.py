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

import time

#Pomas: 2, Tinka: 0
UART_PORTNO = 2
#Pomas: 'B8', Tinka: 'B6
EN_PIN = 'B8'

#wifiname and wifipassword
WIFI_NAME = '[wifi name]'
WIFI_PASSWORD = '[wifi password]'

#MQTT
#(1) NUWALab
NUWA_USERNAME = '[NUWA MQTT username]'
NUWA_PASSWORD = '[NUWA MQTT password]'
NUWA_SERVER = '[NUWA MQTT server]'
NUWA_PORTNO = '[NUWA MQTT server port]'
#(2) Webduino
Webduino_USERNAME = '[Webduino MQTT username]'
Webduino_PASSWORD = '[Webduino MQTT password]'
Webduino_SERVER = '[Webduino MQTT server]'
Webduino_PORTNO = '[Webduino MQTT server port]'
#(3) NUTN
NUTN_USERNAME = '[NUTN MQTT username]'
NUTN_PASSWORD = '[NUTN MQTT password]'
NUTN_SERVER = '[NUTN MQTT server]'
NUTN_PORTNO = '[NUTN MQTT server port]'

#(4) MQTT Server Option
MQTT_USERNAME_List = [NUWA_USERNAME, Webduino_USERNAME, NUTN_USERNAME]
MQTT_PASSWORD_List = [NUWA_PASSWORD, Webduino_PASSWORD, NUTN_PASSWORD]
MQTT_SERVER_List = [NUWA_SERVER, Webduino_SERVER, NUTN_SERVER]
MQTT_PORTNO_List = [NUWA_PORTNO, Webduino_PORTNO, NUTN_PORTNO]
#(5) Adopted MQTT
MQTT_Index = 2 #0: NUWA Server, 1: Webduino Server, 2: NUTN Server
MQTT_USERNAME = MQTT_USERNAME_List [MQTT_Index]
MQTT_PASSWORD = MQTT_PASSWORD_List [MQTT_Index]
MQTT_SERVER = MQTT_SERVER_List [MQTT_Index]
MQTT_PORTNO = MQTT_PORTNO_List [MQTT_Index]
MQTT_CLIENTID = 'nutn_' + str(time.time())

MQTT_Publish_Count = 2

MQTT_AIFMLTOPIC = 'TxIi925'
MQTT_MOONCARTOPIC = 'speak1'
MQTT_NUWATOPIC = 'run1'
MQTT_CHKRECV_COUNT = 1
MQTT_WaitTime = 4000
MQTT_pqos = '2'
MQTT_retain = '0'

#two-way MQTT Function (publish and subscribe)
MQTT_AIFMLTOPIC_Subscriber = 'TxIi925'
MQTT_AIFMLTOPIC_Publisher = 'TxIi925_pub'
MQTT_Publish_Separator = '_'
MQTT_Publish_Count = 2

#ADAS: Manual (=False) or Automatic(=True)
ADAS_Automatic = True
#ADAS: Filter unreasonable Ultrasound distance
ADAS_MaxcountFarDistance = 2
#ADAS: Activate Camera (=True) or not (=False)
ADAS_Camera = False

#LCD
LCDImgDelayTime = 500
LCDStartX = 1
LCDStartY = 60
LCDPhotoDelayTime = 200



