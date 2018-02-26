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

class PathLoss:
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

class ShadowFading:
    ''' Shadowing 2D model '''
    def __init__(self, n=const.N_SH, sigma=const.SD, mean=const.M_SH):
        self.n = n
        self.sd = sigma
        self.m = mean
        self.shw_map = np.random.normal(self.m, self.sd, (n,n))

class FastFading:
    ''' Fast Fading model - Rayleigh fading '''
    pass

class Noise:
    ''' Noise signal '''
    pass

class Interference:
    ''' Interference from others cells '''
    pass

class Channel:
    ''' Channel model class'''
    def __init__(self, env=const.ENV, fc=const.FC):
        self.path_loss = PathLoss(env=env, fc=fc)
        self.shadow = ShadowFading()
  