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
import nomalib.utils as utl
from nomalib.utils import Coordinate as Coord
import nomalib.constants as const
import nomalib.devices as dev

class Grid:
    ''' Hexagonal grid with 19 eNodeBs 
        Radius = R, Inter-Site Distance = 3R e Cell Range = 2R'''
    def __init__(self, r=const.R_CELL):
        self.r = r
        self.user_equipments = np.array([])
        self.base_stations = np.array([])
        self.h = np.sqrt(3)*r
        self.coordinates= np.array(
            [Coord(-3*r, -3*self.h), Coord(0, -3*self.h), Coord(3*r, -3*self.h),
             Coord(-4.5*r, -1.5*self.h), Coord(-1.5*r, -1.5*self.h), Coord(1.5*r, -1.5*self.h), Coord(4.5*r, -1.5*self.h),
             Coord(-6*r, 0), Coord(-3*r, 0), Coord(0, 0), Coord(3*r, 0), Coord(6*r, 0),
             Coord(-4.5*r, 1.5*self.h), Coord(-1.5*r, 1.5*self.h), Coord(1.5*r, 1.5*self.h), Coord(4.5*r, 1.5*self.h),
             Coord(-3*r, 3*self.h), Coord(0, 3*self.h), Coord(3*r, 3*self.h)])
        self.hex = utl.Hexagon(self.r*8)

    ''' Deploy all user equipments on grid with uniform distribution'''
    def deploy_user_equipment(self, n_ue=const.N_UE):
        coords = np.array([])
        while (coords.size < n_ue):
            x = np.random.uniform(-8*self.r, 8*self.r)
            y = np.random.uniform(-4*self.h, 4*self.h)
            if (self.hex.f(x,'bottom') < y < self.hex.f(x,'upper')):
                coords = np.append(coords, Coord(x,y))
        for i in range(n_ue):
            self.user_equipments = np.append(self.user_equipments, dev.UserEquipment(i+1001, coords[i]))
    ''' Deploy base stations with fix grid coordinates'''
    def deploy_base_station(self, n_bs=const.N_BS):
        for i in range(n_bs):
            self.base_stations = np.append(self.base_stations, dev.BaseStation(i+101, self.coordinates[i]))


