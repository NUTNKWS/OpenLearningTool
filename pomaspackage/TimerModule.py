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

class TimerModule():
    def __init__(self):
        return

    def get_CurrentTime(self):        
        timestruct = time.localtime(time.time())
        #time.struct_time(tm_year=2018, tm_mon=2, tm_mday=8, tm_hour=13, tm_min=37, tm_sec=31, tm_wday=3, tm_yday=39, tm_isdst=0)
        tm_year = timestruct[0]
        tm_mon = timestruct[1]
        tm_mday = timestruct[2]
        tm_hour = timestruct[3]
        tm_min = timestruct[4]
        tm_sec = timestruct[5]       
        self.timestamp = str(tm_year) + '-' + str(tm_mon) + '-' + str(tm_mday) + '-' + str(tm_hour) + '-' + str(tm_min) + '-' + str(tm_sec)
        print('TimeStamp: ', self.timestamp)
        return self.timestamp
        
