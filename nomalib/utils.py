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

# classes

class Coordinate:
    ''' Coordinate x and y'''
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Hexagon:
    ''' Hexagon shape of cell'''
    def __init__(self,r, center=Coordinate(0,0)):
        self.r = r
        self.c = center
    
    def f(self, x):
        x = x-self.c.x
        h = 0
        if (0 <= x < .5*self.r):
            h = np.sqrt(3)*.5*self.r
        elif (.5*self.r <= x < self.r):
            h =np.sqrt(3)*.5*self.r -np.sqrt(3)*x
        return h