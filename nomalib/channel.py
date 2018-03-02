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
from nomalib.utils import Coordinate as Coord

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

class Noise:
    ''' Noise signal '''
    pass

class ShadowFading:
    ''' Shadow fading 2D map with uncorrelated lognormal distribution'''
    def __init__(self, mean=const.SHW_M, std=const.SHW_STD, den=const.SHW_D, r=const.R_CELL):
        self.den = d = den
        self.width = w = 16*r
        self.hight = h = 8*np.sqrt(3)*r
        self.c = Coord(w/2, h/2)
        self.mean = mean
        self.std = std
        px_w = int(round(w/d))
        px_h = int(round(h/d))
        self.shw_map = np.random.normal(size=(px_h, px_w))

    def inter_site_corr(self, s, corr=const.R_SITE):
        ''' Shadown fading 2D maps with fix correlation R_SHW '''
        self.shw_map = np.sqrt(corr)*s+(1-np.sqrt(corr))*self.shw_map

    def cross_correlation(self):
        # 12 neighbor matrix
        n = np.array([[11, 5, 10, 6, 12],
                      [7, 1, 2, 3, 8],
                      [9, 4, 13]])
        dist = np.zeros(n.size, n.size)
        for i in range(len(n)):
            for j in range(len(n[i])):

        pass
    
    def save_shadow_map(self, file='shadow.npy'):
        ''' Save numpy array with shadow map to file'''
        np.save(const.SHW_PATH+file,self.shw_map)

class FastFading:
    ''' Fast Fading model - Rayleigh fading '''
    pass

class Interference:
    ''' Interference from others cells '''
    pass

class Channel:
    ''' Channel model class'''
    def __init__(self, env=const.ENV, fc=const.FC):
        self.path_loss = PathLoss(env=env, fc=fc)
        self.noise  = Noise()
        self.shadow = ShadowFading()
        # self.shadow.inter_site_corr(shadow_grid)