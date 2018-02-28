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
from nomalib.utils import Hexagon
from nomalib.utils import Coordinate as Coord
import nomalib.constants as const
import nomalib.devices as dev

class Cell:
    ''' Hexagon cell with antenna in the corner
        id = 1 - fc_type = 1 - from -60 to 60
        id = 3 - fc_type = 2 - from 60 to 180
        id = 2 - fc_type = 3 - from 180 to 300 '''
    def __init__(self, id, r=const.R_CELL):
        self.id = id
        self.r = r
        self.freq_type = id % 10
        self.center = center
        self.ue_ids = []

class Site:
    ''' Site with Radius = R, Inter-Site Distance = 3R e Cell Range = 2R '''
    def __init__(self, id, coord, n_sec=const.N_SEC):
        self n_sec = n_sec
        self.bs = dev.BaseStation(id, coord)
    def start_base_station(self):
        ''' Start BS and create cells '''
        deg = 360/self.n_sec
        t_start = np.deg2rad(0)
        t_step = alpha = np.deg2rad(deg)
        for i in range(self.n_sec):
            x = self.coord.x + np.cos(alpha*i)*const.R_CELL
            y = self.coord.y + np.sin(alpha*i)*const.R_CELL
            c = Cell(self, (self.id*10+i+1), BSAntenna((t_start+i*t_step)), i, Coord(x, y))
            self.cells = np.append(self.cells, c)
        self.status = 'on'
        self.started = True
        
        self.status = 'off'
        self.started = False

    def start_base_station(self):
        ''' Start BS and create cells '''
        deg = 360/self.n_sec
        t_start = np.deg2rad(0)
        t_step = np.deg2rad(deg)
        for i in range(self.n_sec):
            self.antenna.append(BSAntenna(theta_d=t_start+i*t_step))
        self.status = 'on'
        self.started = True


    def get_cell(self, cell_id):
        ''' Return cells from cell_id '''        
        if self.started:
            for c in self.cells:
                if (c.id == cell_id):
                    return c
        logger.warn("BS don't started. 'None' type will be returned")
        return None


class Grid:
    ''' Hexagonal grid with 19 Sites '''
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
        self.hex = Hexagon(self.r*8)

    ''' Deploy all user equipments on hexagon or square grid with uniform distribution'''
    def deploy_user_equipment(self, region='square', n_ue=const.N_UE):
        coords = np.array([])
        if region=='hexagon':
            while (coords.size < n_ue):            
                x = np.random.uniform(-8*self.r, 8*self.r)
                y = np.random.uniform(-4*self.h, 4*self.h)
                if (self.hex.f(x,'bottom') < y < self.hex.f(x,'upper')):
                    coords = np.append(coords, Coord(x,y))
        elif region=='square':
            while (coords.size < n_ue):            
                x, y = np.random.uniform(-8*self.r, 8*self.r, (2))
                coords = np.append(coords, Coord(x,y))
        for i in range(n_ue):
            self.user_equipments = np.append(self.user_equipments, dev.UserEquipment(i+1001, coords[i]))

    ''' Deploy base stations with fix grid coordinates'''
    def deploy_base_station(self, n_bs=const.N_BS):
        for i in range(n_bs):
            self.base_stations = np.append(self.base_stations, dev.BaseStation(i+101, self.coordinates[i]))

    ''' Start all base station '''
    def start_all_base_stations(self):
        for bs in self.base_stations:
            bs.start_base_station()
    
    ''' Connect one UE to nearest BS '''
    def connect_ue_to_bs(self, ue_id):
        for ue in self.user_equipments:
            if (ue.id == ue_id):
                bs_id = ue.nearest_bs(self.base_stations)
                ue.connect_to_bs(bs_id)
                bs = self.get_bs(bs_id)
                bs.ue_ids = np.append(bs.ue_ids, ue.id)
    
    ''' Connect one UE to cell'''
    def connect_ue_to_cell(self, ue_id, ch):
        ue = self.get_ue(ue_id)
        cell_id = ue.best_cell(self.base_stations, ch)
        ue.connect_to_cell(cell_id)
        c = self.get_cell(cell_id)
        c.ue_ids = np.append(c.ue_ids, ue.id)

    ''' Connect all UE's to nearest BS '''
    def connect_all_to_bs(self):
        for ue in self.user_equipments:
            self.connect_ue_to_bs(ue.id)

    ''' Connect all UE's to the best cell '''
    def connect_all_to_cell(self, ch):
        for ue in self.user_equipments:
            self.connect_ue_to_cell(ue.id, ch)

    ''' Return BS from ID '''
    def get_bs(self, id):
        for bs in self.base_stations:
            if (bs.id == id):
                return bs
        return None

    ''' Return Cell from ID '''
    def get_cell(self, id):
        for bs in self.base_stations:
            for c in bs.cells:
                if (c.id == id):
                    return c
        return None
    
    ''' Return UE from ID '''
    def get_ue(self, id):
        for ue in self.user_equipments:
            if (ue.id == id):
                return ue
        return None