#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 07/05/2018
# Version: 1.1

# Python module for NOMA communications simulations
# The devices classes are declared here

# modules
import numpy as np
from logzero import logger
import nomalib.constants as const
import nomalib.channel as ch
import nomalib.utils as utl
from nomalib.utils import Coordinate as Coord

# classes

class BSAntenna:
    ''' Base Station Antenna '''
    def __init__(self, theta_d=0, gain=const.G_BS):
        self.theta_d = theta_d
        self.gain = gain

    def radiation_pattern(self, theta, theta3db=const.THT_3DB, att_max=const.ATT_MAX):
        ''' Radiation Pattern '''        
        theta = theta - self.theta_d
        if (abs(theta) > np.pi):
            theta = theta - (theta/abs(theta))*2*np.pi
        a = 12*((theta/np.radians(theta3db))**2)
        return (-1)*np.min([a,att_max])

class UEAntenna:
    ''' User Equipment Antenna '''
    def __init__(self, gain=const.G_UE):
        self.gain = gain

    def radiation_pattern(self, theta):
        ''' Radiation Pattern Omni-directional'''        
        return 0

class BaseStation:
    ''' Base Station - eNodeB '''
    def __init__(self, id, coord, hight=const.H_BS, pwr_max=const.PW_BS_MAX, n_sector=const.N_SEC):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr_max = pwr_max
        self.n_sec = n_sector
        self.live = False

class UserEquipment:
    ''' Equipment of User '''
    def __init__(self, id, coord, hight=const.H_UE, pwr_max=const.PW_UE_MAX):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr_max = pwr_max
        self.cell_id = None
        self.cell_fr = None
        self.live = True
        self.antenna = UEAntenna()
        self.connected = False
    
    def distance_to(self,dev):
        '''  Calculate distante to any device [km]'''
        dx = abs(self.coord.x-dev.coord.x)
        dy = abs(self.coord.y-dev.coord.y)
        distance = np.sqrt(dx**2 + dy**2)/1000
        return distance

    def angle_from(self, dev):
        ''' Return angle in rad from device coordinate ''' 
        dx = self.coord.x-dev.coord.x
        dy = self.coord.y-dev.coord.y
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

    def received_power(self, site, cell_id, mode='subband'):
        ''' Calculates power received from BS '''
        cell = site.get_cell(cell_id)
        bs = site.bs
        ch = site.channel
        tx_pwr = {'subband':cell.pwr, 'total':bs.pwr_max}
        dist = self.distance_to(bs)
        theta = self.angle_from(bs)
        att = ch.path_loss.attenuation(dist) + ch.shadow.get_shw(self.coord)\
            - cell.antenna.gain - self.antenna.gain
        rx_pwr = tx_pwr[mode] - np.maximum(att, const.MCL)\
                + cell.antenna.radiation_pattern(theta)
        return rx_pwr
    
    def received_power_connected(self, sites, mode='subband'):
        ''' Calculates power received from the BS that UE is connected '''
        if (self.connected):
            bs_idx, cell_idx = utl.ids2index(self.cell_id)
            return self.received_power(sites[bs_idx], self.cell_id, mode=mode)
        else:
            logger.error("UE don't connnected to one BS ")

    def received_interference(self, sites, mode='subband'):
        ''' Calculates received interference from the others BS '''
        rx_inter = []
        if (self.connected):
            for site in sites:
                for cell in site.cells:
                    if (self.cell_id != cell.id and self.cell_fr == cell.fr):
                        rx = self.received_power(site, cell.id, mode=mode)
                        rx_inter.append(rx)
        else:
            logger.error("UE don't connnected to one BS")
        return np.array(rx_inter)

    def best_cell(self, sites, tti=0):
        ''' Return id of Cell with the best power '''
        # define initial condition
        e = False
        for site in sites:
            best_site = site
            for cell in site.cells:
                if (cell.accept_ue):
                    best_cell = cell
                    e = True
                    break
            if (e):
                break
        for site in sites:
            for cell in site.cells:
                if (cell.accept_ue):
                    if (self.received_power(site, cell.id, mode='total') >\
                    self.received_power(best_site, best_cell.id, mode='total')):
                        best_site = site
                        best_cell = cell
        return best_cell.id

    def connect_to_cell(self, cell):
        ''' Connect UE to Cell with cell_id '''        
        self.cell_id = cell.id
        self.cell_fr = cell.fr
        self.connected = True
    
    def disconnect_to_cell(self, cell):
        ''' Disconnect UE to Cell with cell_id '''        
        self.cell_id = None
        self.cell_fr = None
        self.connected = False