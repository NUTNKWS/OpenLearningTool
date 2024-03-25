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


import const

stored_data = ['Today is Thursday and a funny day.',
                'I am working with the QCI&AI Learning Tool.']

if __name__ == '__main__':

    mySD = pomaspkg.SDModule()
    #readfile
    data = mySD.ReadFile('./sd/input/test.py')
    print (data)

    #write and delete file (Note: You can see the executed resule after reset the board)
    mySD.WriteFile('./sd/output/test.txt', stored_data, 'w')
    mySD.DeleteFile('./sd/output/test.py')