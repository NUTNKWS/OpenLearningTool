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

from machine import Pin

class ButtonModule():
    def __init__(self, lcd):

        #big Button
        self.btnGREEN1 = Pin('C0',Pin.IN)
        self.btnYELLOW = Pin('C1',Pin.IN)
        self.btnRED1 = Pin('C2',Pin.IN)
        self.btnGREEN2 = Pin('C3',Pin.IN)
        self.btnRED2 = Pin('F0',Pin.IN)
        self.btnList = [self.btnGREEN1, self.btnYELLOW, self.btnRED1, self.btnGREEN2, self.btnRED2]

        #small Button
        self.btn1 = Pin('E6', Pin.IN)
        self.btn2 = Pin('E7', Pin.IN)
        self.keybtnList = [self.btn1, self.btn2]
        
        self.lcd = lcd

    def getButtonPressed(self, index):
        '''
        Function: Check if there is any button pressed
        Input:
        (1) index: data's index
        Output: data's index
        
        '''    
        data_index = index
        for i in range(len(self.btnList)):
            if (self.btnList[i].value() == 0):
                #pressed is 0
                button_index = i
                msg = 'Clicking on BtnNo. {}'.format(button_index + 1)
                print(msg)
                self.lcd.ShowMessage_LCD(msg)
                return button_index

        return data_index
    
    def getKeyPressed(self, index):
        data_index = index
        for i in range(len(self.keybtnList)):
            if (self.keybtnList[i].value() == 1):
                #pressed is 1
                button_index = i
                msg = 'Clicking on KeyBtnNo. {}'.format(button_index + 1)
                print(msg)
                self.lcd.ShowMessage_LCD(msg)
                return button_index

        return data_index
    
    def getbtnYELLOWState(self):
        return self.btnYELLOW.value()
        

    
            