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
import nomalib.utils as utl
from nomalib.utils import Coordinate as Coord
import nomalib.constants as const
import nomalib.devices as dev

class Grid:
    ''' Hexagonal grid with 19 eNodeBs 
        Radius = R, Inter-Site Distance = 3R e Cell Range = 2R'''
    def __init__(self, r=const.R_CELL):
        self.r = r
        self.users = np.array([])
        self.h = np.sqrt(3)*r
        self.coordinates= np.array(
            [Coord(-3*r, -3*self.h), Coord(0, -3*self.h), Coord(3*r, -3*self.h),
             Coord(-4.5*r, -1.5*self.h), Coord(-1.5*r, -1.5*self.h), Coord(1.5*r, -1.5*self.h), Coord(4.5*r, -1.5*self.h),
             Coord(-6*r, 0), Coord(-3*r, 0), Coord(0, 0), Coord(3*r, 0), Coord(6*r, 0),
             Coord(-4.5*r, 1.5*self.h), Coord(-1.5*r, 1.5*self.h), Coord(1.5*r, 1.5*self.h), Coord(4.5*r, 1.5*self.h),
             Coord(-3*r, 3*self.h), Coord(0, 3*self.h), Coord(3*r, 3*self.h)])
        self.hex = utl.Hexagon(self.r*8)

    def deploy_users_equipment(self, n_users=const.N_UE):
        coords = np.array([])
        while (coords.size < n_users):
            x = np.random.uniform(-8*self.r, 8*self.r)
            y = np.random.uniform(-4*self.h, 4*self.h)
            if (self.hex.f(x,'bottom') < y < self.hex.f(x,'upper')):
                coords = np.append(coords, Coord(x,y))
        for i in range(n_users):
            self.users = np.append(self.users, dev.UserEquipment(id=i, coord=coords[i]))
            
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

class Cell:
    pass