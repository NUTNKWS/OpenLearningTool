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

class StatAnalModule():
    def __init__(self):
        return
        
    def mymin(self, v1, v2):
        if v1 > v2:
            return v2
        return v1

    def mymax(self, v1, v2):
        if v1 > v2:
            return v1
        return v2

    def get_mean(self, values):
        n = len(values)
        return sorted(values)[n // 2]

    def get_median(self, values):
        """ Calculates median of values """
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 1:
            # Take middle value
            return sorted_values[n // 2]
        else:
            # Take average of 2 values at center
            v = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
            #print('v=', v)
            return v