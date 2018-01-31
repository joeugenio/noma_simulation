#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 30/01/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The channel model classes are declared here

# modules
import numpy as np
import nomalib.constants as const

# classes

class PropagationModel:
    ''' Distance dependent propagation model '''
    def __init__(self, env=const.ENV, fc=const.FC):
        self.env = env
        self.fc = fc

    def attenuation(self, d):
        try:
            d_db = np.log10(d)
        except ZeroDivisionError:
            d_db = float('-Inf')
        
        if (self.env=='urban' and self.fc==900):
            l = 120.9 + 36.7*d_db
        elif (self.env=='urban' and self.fc==2000):
            l = 128.1 + 36.7*d_db
        elif (self.env=='rural' and self.fc==900):
            l = 95.5 + 34.1*d_db
        else: print('ERROR: invalid frequency or environment')

        return l

class Shadowing:
    ''' Shadowing 2D model '''
    