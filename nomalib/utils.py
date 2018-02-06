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
    
    def f(self, x_arg):
        x_size = len(x_arg)
        y_u = np.zeros(x_size)
        y_b = np.zeros(x_size)
        x = np.zeros(x_size)
        for i in range(x_size):
            x[i] = x_arg[i]-self.c.x
            if (0 <= abs(x[i]) < .5*self.r):
                y_u[i] = self.r*.5*np.sqrt(3)
            elif (.5*self.r <= abs(x[i]) <= self.r):
                y_u[i] = (self.r-abs(x[i]))*np.sqrt(3)
            y_b[i] = (-1)*y_u[i]
            y_u[i] = y_u[i] + self.c.y
            y_b[i] = y_b[i] + self.c.y
        return (y_u,y_b)
    
    def f_upper(self, x_arg):
        return self.f(x_arg)[0]
    
    def f_bottom(self, x_arg):
        return self.f(x_arg)[1]