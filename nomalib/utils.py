#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 01/02/2018
# Version: 1.0

# Python module for NOMA communications simulations
# The utils classes are declared here

import numpy as np
import nomalib.constants as const

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