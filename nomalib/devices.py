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
import nomalib.constants as const
from nomalib.utils import Coordinate

# classes

class BSAntenna:
    ''' Base Station Antenna '''
    def __init__(self, theta_min, bs_gain = const.G_BS):
        self.theta_min = theta_min
        self.bs_gain = bs_gain
        
    ''' Radiation Pattern '''
    def radiation_pattern(self, theta, theta3db=65, att_max=20):
        a = 12*(theta/np.radians(theta3db))**2
        return (-1)*np.min([a,att_max])

class UEAntenna:
    ''' User Equipment Antenna '''
    def __init__(self, ue_gain = const.G_UE):
        self.ue_g = ue_gain
    
    ''' Radiation Pattern Omni-directional'''
    def radiation_pattern(self, theta):
        return 0

class Cell:
    ''' Cell (Sector)
        id = 1 - from -60 to 60
        id = 3 - from 60 to 180
        id = 2 - from 180 to 300'''
    def __init__(self, antenna:BSAntenna, id:int, r=const.R_CELL, bs_id=None):
        self.ant = antenna
        self.id = id
        self.r = r
        self.bs_id = bs_id

class BaseStation:
    ''' Base Station - eNodeB '''
    def __init__(self, id:int, coord:Coordinate, hight=const.H_BS, power=const.PW_BS, n_sector=const.N_SEC):
        self.id = id
        self.h = hight
        self.pwr = power
        self.n_sec = n_sector   
        self.coord = coord
        self.status = 'off'
        self.ue_id = np.array([])
        self.cells = np.array([])

    ''' Start BS and create cells'''
    def startBS(self):
        t_start = np.deg2rad(-60)
        t_step = np.deg2rad(120)
        for i in range(const.N_SEC):
            c = Cell((self.id*10+i+1),BSAntenna((t_start+i*t_step)))
            self.cells = np.append(self.cells, c)
        self.status = 'on'

class UserEquipment:
    ''' Equipment of User '''
    def __init__(self, id:int, coord:Coordinate, hight=const.H_UE, power=const.PW_UE):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr = power
        self.bs_id = None
    
    def received_power(self):
        rx_pwr = tx_pwr-np.max([path_loss-const.BS_G-const.UE_G, const.MCL])
        return rx_pwr

    def connect(self):
        pass

# function of module
def index2id(i):
    pass
# l.index
