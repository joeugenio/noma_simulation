#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 28/02/2018
# Version: 1.1

# Python classes for NOMA communications simulations
# The scenarios are defined based on 3GPP TR 36.942 v14.0.0

import numpy as np
from logzero import logger
from nomalib.utils import Hexagon
from nomalib.utils import Coordinate as Coord
import nomalib.constants as const
import nomalib.devices as dev
import nomalib.channel as ch

class Cell:
    ''' Hexagon cell with antenna in the corner
        id = 1 - fc_type = 1 - from -60 to 60
        id = 3 - fc_type = 2 - from 60 to 180
        id = 2 - fc_type = 3 - from 180 to 300 '''
    def __init__(self, id, bs, freq_reuse, r=const.R_CELL):
        self.id = id
        self.r = r
        self.fr = freq_reuse
        self.angle = np.deg2rad(360/bs.n_sec)
        x = bs.coord.x + np.cos(self.angle*(self.fr))*r
        y = bs.coord.y + np.sin(self.angle*(self.fr))*r
        self.center = Coord(x,y)
        self.antenna = dev.BSAntenna(self.angle*freq_reuse)
        self.ue_ids = []

class Site:
    ''' Site with Radius = R, Inter-Site Distance = 3R e Cell Range = 2R '''
    def __init__(self, id, coord, n_sec=const.N_SEC):
        self.n_sec = n_sec
        self.bs = dev.BaseStation(id, coord)
        self.channel = ch.Channel(id)
        self.cells = []

    def start_base_station(self):
        ''' Start BS and create cells '''
        for i in range(self.n_sec):
            c = Cell((self.bs.id*10+i+1), self.bs, i)
            self.cells.append(c)
        self.bs.live = True

    def get_cell(self, cell_id):
        ''' Return cells from cell_id '''        
        if self.bs.live:
            for c in self.cells:
                if (c.id == cell_id):
                    return c
        logger.warn("BS "+str(self.bs.id)+" don't started. 'None' type will be returned")
        return None

class Grid:
    ''' Hexagonal grid with 19 Sites '''
    def __init__(self, n_bs=const.N_BS, r=const.R_CELL):
        self.r = r
        self.n_bs = n_bs
        self.user_equipments = []
        self.sites = []
        h_cell = np.sqrt(3)*r
        self.width = 16*r
        self.hight = 8*h_cell
        self.coordinates= [Coord(-3*r, -3*h_cell), Coord(0, -3*h_cell), Coord(3*r, -3*h_cell),
             Coord(-4.5*r, -1.5*h_cell), Coord(-1.5*r, -1.5*h_cell), Coord(1.5*r, -1.5*h_cell), Coord(4.5*r, -1.5*h_cell),
             Coord(-6*r, 0), Coord(-3*r, 0), Coord(0, 0), Coord(3*r, 0), Coord(6*r, 0),
             Coord(-4.5*r, 1.5*h_cell), Coord(-1.5*r, 1.5*h_cell), Coord(1.5*r, 1.5*h_cell), Coord(4.5*r, 1.5*h_cell),
             Coord(-3*r, 3*h_cell), Coord(0, 3*h_cell), Coord(3*r, 3*h_cell)]
        self.hex = Hexagon(r=self.width/2)

    def deploy_user_equipment(self, region='square', n_ue=const.N_UE):
        ''' Deploy all user equipments on hexagon or square grid with uniform distribution'''
        coords = []
        if region=='hexagon':
            while (len(coords) < n_ue):
                x = np.random.uniform(-self.width/2, self.width/2)
                y = np.random.uniform(-self.hight/2, self.hight/2)
                if (self.hex.f(x,'bottom') < y < self.hex.f(x,'upper')):
                    coords.append(Coord(x,y))
        elif region=='square':
            while (len(coords) < n_ue):            
                x, y = np.random.uniform(-self.width/2, self.width/2, (2))
                coords.append(Coord(x,y))
        for i in range(n_ue):
            self.user_equipments.append(dev.UserEquipment(i+1001, coords[i]))

    def deploy_base_station(self):
        ''' Deploy base stations with fix grid coordinates'''
        for i in range(self.n_bs):
            self.sites.append(Site(i+101, self.coordinates[i]))

    def start_all_base_stations(self):
        ''' Start all base station '''
        for s in self.sites:
            s.start_base_station()
  
    ''' Connect one UE to cell'''
    def connect_ue_to_best_cell(self, ue_id):
        ue = self.get_ue(ue_id)
        cell_id = ue.best_cell(self.sites)
        ue.connect_to_cell(cell_id)
        c = self.get_cell(cell_id)
        c.ue_ids.append(ue.id)

    ''' Connect all UE's to the best cell '''
    def connect_all_ue(self):
        for ue in self.user_equipments:
            self.connect_ue_to_best_cell(ue.id)

    ''' Return BS from ID '''
    def get_bs(self, id):
        for s in self.sites:
            if (s.bs.id == id):
                return s.bs
        return None

    ''' Return Cell from ID '''
    def get_cell(self, id):
        for s in self.sites:
            for c in s.cells:
                if (c.id == id):
                    return c
        return None
    
    ''' Return UE from ID '''
    def get_ue(self, id):
        for ue in self.user_equipments:
            if (ue.id == id):
                return ue
        return None