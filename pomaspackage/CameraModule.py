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

import sensor

class CameraModule():
    def __init__(self):
        #set the size of the output image
        sensor.set_framesize(1)
        sensor.start()
        #set horizontal flip
        sensor.set_hmirror(1)


    def ShowSnapShot(self):
        #get image from camera
        img = sensor.snapshot()
        return img


