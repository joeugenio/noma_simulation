#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 31/01/2018
# Version: 1.0

# Python classes for NOMA communications simulations
# The scenarios are defined based on 3GPP TR 36.942 v14.0.0

import numpy as np
from logzero import logger
from nomalib.utils import Coordinate as Coord
import nomalib.constants as const
import nomalib.devices as dev

class Area:
    ''' Interest area '''
    def __init__(self, width:int, hight:int):
        self.w = width
        self.h = hight

class Grid:
    ''' Hexagonal grid with 19 eNodeBs 
        Radius = R, Inter-Site Distance = 3R e Cell Range = 2R'''
    def __init__(self,r):
        self.users = []
        self.r = r
        self.coord = [Coord(5*r, np.sqrt(3)*r), Coord(8*r, np.sqrt(3)*r), Coord(11*r, np.sqrt(3)*r),
                      Coord(3.5*r, 2.5*np.sqrt(3)*r), Coord(6.5*r, 2.5*np.sqrt(3)*r), Coord(9.5*r, 2.5*np.sqrt(3)*r), Coord(12.5*r, 2.5*np.sqrt(3)*r),
                      Coord(2*r, 4*np.sqrt(3)*r), Coord(5*r, 4*np.sqrt(3)*r), Coord(8*r, 4*np.sqrt(3)*r), Coord(11*r, 4*np.sqrt(3)*r), Coord(14*r, 4*np.sqrt(3)*r),
                      Coord(3.5*r, 5.5*np.sqrt(3)*r), Coord(6.5*r, 5.5*np.sqrt(3)*r), Coord(9.5*r, 5.5*np.sqrt(3)*r), Coord(12.5*r, 5.5*np.sqrt(3)*r),
                      Coord(5*r, 7*np.sqrt(3)*r), Coord(8*r, 7*np.sqrt(3)*r), Coord(11*r, 7*np.sqrt(3)*r)]

        x_ori = self.r*8
        y_ori = self.r*7
        for c in self.coord:
            c.x = c.x-x_ori
            c.y = c.y-y_ori

    def deploy_users_equipment(self, n_user=const.N_UE):
        x = np.random.uniform(-self.r*9, self.r*9, n_user)
        y = np.random.uniform(-self.r*8, self.r*8, n_user)

        for i in range(n_user):
            self.users += [dev.UserEquipment(id=i, coord=Coord(x[i],y[i]))]
            




class Area:
    ''' Interest area '''
    def __init__(self, width:int, hight:int):
        self.w = width
        self.h = hight

class Cell:
    ''' Three hexagonal sectors cell'''
    def __init__(self, r, pos:Coord):
        self.r = r
        self.p = pos

    # upper left limit of hexagon
    def ull(self, x):
        return np.sqrt(3)*(x)
    # upper center limit of hexagon
    def ucl(self, x):
        return self.r*np.sqrt(3)*.5*(x/x)
    # upper right limit of hexagon
    def url(self, x):
        return (2*self.r-x)*np.sqrt(3)
    # lower left limit of hexagon
    def lll(self, x):
        return (-1)*np.sqrt(3)*(x)
    # lower center limit of hexagon
    def lcl(self, x):
        return (-1)*self.r*np.sqrt(3)*.5*(x/x)
    # lower right limit of hexagon
    def lrl(self, x):
        return (x-2*self.r)*np.sqrt(3)

    # determine if one coordinate is in cell region
    def in_or_out(self, c:Coord):
        x = c.x-self.p.x
        cond_l = cond_c = cond_r = False
        if (0 <=  x < .5*self.r):
            if (self.lll(x) <= c.y-self.p.y <= self.ull(x)):
                cond_l = True
        elif (.5*self.r <= x < 1.5*self.r):
            if (self.lcl(x) <= c.y-self.p.y <= self.ucl(x)):
                cond_c = True
        elif (1.5*self.r <= x < 2*self.r):
            if (self.lrl(x) <= c.y-self.p.y <= self.url(x)):
                cond_r = True
        if (cond_l or cond_c or cond_r):
            return 'in'
        else:
            return 'out'


class Site:
    ''' Site with 3 sectors '''
    def __init__(self, r, pos=Coord(0,0)):
        self.r = r
        self.p = pos
        self.c1 = Cell(r, Coord(self.p.x-1.5*r, self.p.y-np.sqrt(3)*r*.5))
        self.c2 = Cell(r, Coord(self.p.x-1.5*r, self.p.y+np.sqrt(3)*r*.5))
        self.c3 = Cell(r, Coord(self.p.x, self.p.y))

    def in_or_out(self, c):
        check = [self.c1.in_or_out(c), self.c2.in_or_out(c), self.c3.in_or_out(c)]

        if ('in' in check):
            return 'in'
        else:
            return 'out'
