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

import image, display
from gpb import delay

import const

class LcdModule():
    def __init__(self):
        #enableDisplay
        display.start()
        #clear LCD
        img = self.Clear_LCD()
        
    def Clear_LCD(self):
        img = image.Image(320, 240, image.RGB565)
        display.set_frame(img)
        return img

    def ShowMessage_LCD(self, receivedmsg):
        img = self.Clear_LCD()
        img.draw_string(const.LCDStartX, const.LCDStartY, receivedmsg, (255, 0, 0), scale=3, mono_space=False)
        display.set_frame(img) 

    def ShowImage_LCD(self, filename, delaytime):           
        img = image.Image('./img/' + filename)
        display.set_frame(img)
        delay(delaytime)

    def ShowSnapShot_LCD(self, img, delaytime):
        display.set_frame(img)
        delay(delaytime)
    
    def Show_LCD(self, img, delaytime):
        display.set_frame(img)
        delay(delaytime)
