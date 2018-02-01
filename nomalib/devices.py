#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 30/01/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The devices classes are declared here

# modules
import numpy as np
import constants as const

# classes

class Coordinate:
    ''' Coordinate x and y'''
    def __init__(self,x,y):
        self.x = x
        self.y = y

class BSAntenna:
    ''' Base Station Antenna '''
        def __init__(self, theta_min, bs_gain = const.BSG):
            self.theta_min = theta_min
            self.bs_gain = bs_gain
        
        ''' Radiation Pattern '''
        def radiation_pattern(self, theta, theta3db=65, att_max=20):
            a = 12*(theta/np.radians(theta3db))**2
            return (-1)*np.min([a,att_max])

class UEAntenna:
    ''' User Equipment Antenna '''
        def __init__(self, ue_gain = const.UEG):
            self.ue_g = ue_gain
        
        ''' Radiation Pattern Omni-directional'''
        def radiation_pattern(self, theta):
            return 0

class BaseStation:
    ''' Base Station - eNodeB '''
    def __init__(self, id:str, coord:Coordinate, hight=const.BSH, power=const.BSPW, n_sector=const.):
        self.id = id
        self.h = hight
        self.pwr = power
        self.n_sec = n_sector
        self.coord = coord
        self.ue_id = []

class UserEquipment:
    ''' Equipment of User '''
    def __init__(self, id:str, coord:Coordinate, hight=UEH, power=UEPW):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr = power
        self.bs_id = None
    
    def received_power(self):
        rx_pwr = tx_pwr-np.max()

