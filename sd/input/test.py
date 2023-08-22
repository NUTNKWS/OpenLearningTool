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

import time

#Pomas: 2, Tinka: 0
UART_PORTNO = 2
#Pomas: 'B8', Tinka: 'B6
EN_PIN = 'B8'

#wifiname and wifipassword
WIFI_NAME = '[wifi name]'
WIFI_PASSWORD = '[wifi password]'

#MQTT
#(1) Webduino
Webduino_USERNAME = '[Webduino MQTT username]'
Webduino_PASSWORD = '[Webduino MQTT password]'
Webduino_SERVER = '[Webduino MQTT server]'
Webduino_PORTNO = '[Webduino MQTT server port]'
#(2) NUWALab
NUWA_USERNAME = '[NUWA MQTT username]'
NUWA_PASSWORD = '[NUWA MQTT password]'
NUWA_SERVER = '[NUWA MQTT server]'
NUWA_PORTNO = '[NUWA MQTT server port]'

#(3) Adopted MQTT
MQTT_USERNAME = NUWA_USERNAME
MQTT_PASSWORD = NUWA_PASSWORD
MQTT_SERVER = NUWA_SERVER
MQTT_PORTNO = NUWA_PORTNO
MQTT_CLIENTID = 'nutn_' + str(time.time())

MQTT_AIFMLTOPIC = 'UKcL550'
MQTT_MOONCARTOPIC = 'speak1'
MQTT_NUWATOPIC = 'run1'
MQTT_CHKRECV_COUNT = 1
MQTT_WaitTime = 4000
MQTT_pqos = '2'
MQTT_retain = '0'

#bi-direction (publish and subscribe)
MQTT_AIFMLTOPIC_Subscriber = 'UKcL550'
MQTT_AIFMLTOPIC_Publisher = 'UKcL550_pub'
MQTT_Publish_Separator = '_'

#ADAS
ADAS_Automatic = False

#LCD
LCDImgDelayTime = 500
LCDStartX = 1
LCDStartY = 50
