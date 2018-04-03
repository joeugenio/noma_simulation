#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 01/02/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The utils classes are declared here

# import nomalib.channel as ch
import numpy as np
import nomalib.constants as const
from logzero import logger

# classes

class Coordinate:
    ''' Coordinate x and y'''
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Hexagon:
    ''' Hexagon shape of cell'''
    def __init__(self,r=const.R_CELL, center=Coordinate(0,0)):
        self.r = r
        self.c = center
        self.x_axis = np.linspace(-self.r,self.r,100) + self.c.x
        self.upper = self.f(self.x_axis,'upper')
        self.bottom = self.f(self.x_axis,'bottom')
    
    def f(self, x_arg='None', bounder='upper'):
        if (type(x_arg)==type(np.array([]))):
            pass
        elif (type(x_arg) == type([])):
            x_arg = np.array(x_arg)
        else:
            x_arg = np.array([x_arg])
        y = np.zeros(x_arg.size)
        x = x_arg[:]-self.c.x
        for i in range(x_arg.size):
            if (0 <= abs(x[i]) < .5*self.r):
                y[i] = self.r*.5*np.sqrt(3)
            elif (.5*self.r <= abs(x[i]) <= self.r):
                y[i] = (self.r-abs(x[i]))*np.sqrt(3)
        if (bounder == 'bottom'):
            return (-1)*y + self.c.y
        elif (bounder == 'upper'):
            return y + self.c.y

def get_angle(coord:Coordinate, ori:Coordinate):
    ''' Return angle in rad from x and y coordinate ''' 
    dx = coord.x-ori.x
    dy = coord.y-ori.y
    try:
        tg = dy/dx
    except ZeroDivisionError as e:
        tg = float('Inf')
        logger.debug(e)
    if (dx >= 0 and dy > 0):
        theta = np.arctan(tg)
    elif (dx > 0 and dy <= 0):
        theta = np.deg2rad(360) + np.arctan(tg)
    else:
        theta = np.deg2rad(180) + np.arctan(tg)
    return theta
    
def get_distance(coord:Coordinate, ori:Coordinate):
    ''' Return distance in km from x and y coordinate '''
    dx = coord.x-ori.x
    dy = coord.y-ori.y
    return np.sqrt(dx**2 + dy**2)/1000 

def dbm2watts(dbm):
    ''' Convert power to Watts from dBm '''
    return 10**((dbm-30)/10)

def watts2dbm(watts):
    ''' Convert power to dBm from Watts '''
    return 10*np.log10(1e3*watts)

def get_bs_id(cell_id):
    ''' Get site id from cell id '''
    return int(cell_id/10)

def bsid2index(bs_id):
    ''' Return bs index from bs_id '''
    return bs_id - 101

def ids2index(cell_id):
    ''' Return indexs of bs and cell from cell_id '''
    bs_id = get_bs_id(cell_id)
    bs_i = bsid2index(bs_id)
    return (bs_i, (cell_id % 10) - 1)
    
def index2bsid(i):
    ''' Return bs_id from bs index '''
    return i + 101

def index2cellid(bs_i,cell_i):
    ''' Return cell_id from bs index and cell index '''
    bs_id = index2bsid(bs_i)
    return (bs_id*10 + 1 + cell_i)