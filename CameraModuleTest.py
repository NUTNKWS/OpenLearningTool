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

if __name__ == '__main__':

    myLCD = pomaspkg.LcdModule()
    myCamera = pomaspkg.CameraModule()
    myButton = pomaspkg.ButtonModule(myLCD)
    mySD = pomaspkg.SDModule()
    mySpeaker = pomaspkg.SpeakerModule()
    
    data_index_old = -1
    while True:
        img = myCamera.ShowSnapShot()
        myLCD.ShowSnapShot_LCD(img, const.LCDPhotoDelayTime)
        #check 1st button pressed (1st green button)
        data_index_new = myButton.getButtonPressed(data_index_old)                                        
        #Save the snapshot image to SD
        if (data_index_new == 0):
            #yes, save the photo
            mySpeaker.playAudio('takephoto.mp3')
            #store file
            filename = './sd/output/photo.jpg'
            mySD.WriteImage(filename, img)
            data_index_old = -1
    