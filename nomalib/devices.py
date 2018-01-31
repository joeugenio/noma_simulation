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
