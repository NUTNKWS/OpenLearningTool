
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
    