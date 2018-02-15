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
from logzero import logger
import nomalib.constants as const

# classes

class PropagationModel:
    ''' Distance dependent propagation model '''
    def __init__(self, env=const.ENV, fc=const.FC):
        self.env = env
        self.fc = fc

    def attenuation(self, d):
        if (d == 0):
            d_db = float('-Inf')
            logger.warn('Invalid distance (d = 0.0)')
        else:
            d_db = np.log10(d)
        if (self.env=='urban' and self.fc==900):
            l = 120.9 + 36.7*d_db
        elif (self.env=='urban' and self.fc==2e3):
            l = 128.1 + 36.7*d_db
        elif (self.env=='rural' and self.fc==900):
            l = 95.5 + 34.1*d_db
        else:
            logger.error('Invalid frequency or environment')
            l = 'None'
        return l

class Shadowing:
    ''' Shadowing 2D model '''
    pass

class Noise:
    ''' Noise signal '''
    pass

class Interference:
    ''' Interference from others cells '''
    pass

class PathLoss:
    ''' Path loss model '''
    pass

class Channel:
    ''' Channel model class'''
    def __init__(self, env=const.ENV, fc=const.FC):
        self.propagation = PropagationModel(env=env, fc=fc)