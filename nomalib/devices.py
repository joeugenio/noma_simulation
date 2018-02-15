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
from logzero import logger
import nomalib.constants as const
from nomalib.utils import Coordinate as Coord
import nomalib.utils as utl

# classes

class BSAntenna:
    ''' Base Station Antenna '''
    def __init__(self, theta_d, bs_gain = const.G_BS):
        self.theta_d = theta_d
        self.bs_gain = bs_gain
        
    ''' Radiation Pattern '''
    def radiation_pattern(self, theta, theta3db=65, att_max=20):
        theta = theta - self.theta_d
        if (abs(theta) > np.pi):
            theta = theta - (theta/abs(theta))*2*np.pi
        a = 12*((theta/np.radians(theta3db))**2)
        return (-1)*np.min([a,att_max])

class UEAntenna:
    ''' User Equipment Antenna '''
    def __init__(self, ue_gain = const.G_UE):
        self.ue_g = ue_gain
    
    ''' Radiation Pattern Omni-directional'''
    def radiation_pattern(self, theta):
        return 0

class Cell:
    ''' Cell (Sector)
        id = 1 - from -60 to 60
        id = 3 - from 60 to 180
        id = 2 - from 180 to 300'''
    def __init__(self, bs, id:int, antenna:BSAntenna, frequency_type, center, r=const.R_CELL):
        self.ant = antenna
        self.id = id
        self.r = r
        self.ft = frequency_type
        self.pwr = bs.pwr
        self.coord = bs.coord        
        self.center = center
        self.ue_ids = np.array([])

class BaseStation:
    ''' Base Station - eNodeB '''
    def __init__(self, id:int, coord:Coord, hight=const.H_BS, power=const.PW_BS, n_sector=const.N_SEC):
        self.id = id
        self.h = hight
        self.pwr = power
        self.n_sec = n_sector   
        self.coord = coord
        self.status = 'off'
        self.started = False
        self.ue_ids = np.array([])
        self.cells = np.array([])

    ''' Start BS and create cells '''
    def start_base_station(self):
        t_start = np.deg2rad(0)
        t_step = np.deg2rad(120)
        alpha = np.deg2rad(120)
        for i in range(const.N_SEC):
            x = self.coord.x + np.cos(alpha*i)*const.R_CELL
            y = self.coord.y + np.sin(alpha*i)*const.R_CELL
            c = Cell(self, (self.id*10+i+1), BSAntenna((t_start+i*t_step)), i, Coord(x, y))
            self.cells = np.append(self.cells, c)
        self.status = 'on'
        self.started = True
    
    ''' Return cells from cell_id '''
    def get_cell(self, cell_id):
        if self.started:
            for c in self.cells:
                if (c.id == cell_id):
                    return c
        logger.warn("BS don't started. 'None' type will be returned")
        return None

class UserEquipment:
    ''' Equipment of User '''
    def __init__(self, id:int, coord:Coord, hight=const.H_UE, power=const.PW_UE):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr = power
        self.bs_id = None
        self.cell_id = None
        self.connected = False
    
    ''' Calculate power received on UE '''
    def received_power(self, cell, ch):
        dist = utl.get_distance(self.coord, cell.coord)
        theta = utl.get_angle(self.coord, cell.coord)
        att = ch.propagation.attenuation(dist) - const.G_BS - const.G_UE
        rx_pwr = cell.pwr - np.maximum(att, const.MCL) + cell.ant.radiation_pattern(theta)
        return rx_pwr
    
    ''' Return id of cell and BS with the best power '''
    def best_cell(self, all_bs, ch):
        best_cell = all_bs[0].cells[0]
        for bs in all_bs:
            for c in bs.cells:
                if (self.received_power(c, ch) > self.received_power(best_cell, ch)):
                    best_cell = c
        return best_cell.id
                            
    ''' Connect UE to BS with bs_id '''
    def connect_to_cell(self, cell_id):
        self.cell_id = cell_id
        self.bs_id = cell_id//10
        self.connected = True

    ''' Connect UE to BS with bs_id '''
    def connect_to_bs(self, bs_id):
        self.bs_id = bs_id
        self.connected = True

    '''  Calculate distante to bs'''
    def distance_to_bs(self, bs):
        dx = abs(self.coord.x-bs.coord.x)
        dy = abs(self.coord.y-bs.coord.y)
        distance = np.sqrt(dx**2 + dy**2)
        return distance
    
    ''' Return id of nearest BS '''
    def nearest_bs(self, all_bs):
        n = all_bs[0]
        for bs in all_bs:
            if (self.distance_to_bs(bs) < self.distance_to_bs(n)):
                n = bs
        return n.id
