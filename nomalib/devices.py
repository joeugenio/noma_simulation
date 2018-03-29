#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 27/02/2018
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
    def __init__(self, id, coord, hight=const.H_BS, power=const.PW_BS, n_sector=const.N_SEC):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr = power
        self.n_sec = n_sector
        self.live = False

class UserEquipment:
    ''' Equipment of User '''
    def __init__(self, id, coord, hight=const.H_UE, power=const.PW_UE):
        self.id = id
        self.coord = coord
        self.h = hight
        self.pwr = power
        self.fading = ch.TemporalChannel()
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
    
    def received_power(self, site, cell_id, tti):
        ''' Calculates power received from BS '''
        cell = site.get_cell(cell_id)
        bs = site.bs
        ch = site.channel
        dist = self.distance_to(bs)
        theta = self.angle_from(bs)
        att = ch.path_loss.attenuation(dist) + ch.shadow.get_shw(self.coord) - cell.antenna.gain - self.antenna.gain
        rx_pwr = bs.pwr + self.fading.h.gain[tti] - np.maximum(att, const.MCL) + cell.antenna.radiation_pattern(theta)
        return rx_pwr

    def received_power_connected(self, sites, tti):
        ''' Calculates power received from the BS that UE is connected '''
        if (self.connected):
            for site in sites:
                for cell in site.cells:
                    if (cell.id == self.cell_id):
                        return self.received_power(site, cell.id, tti)
        else:
            logger.error("UE don't connnected to one BS")

    def received_interference(self, sites, tti):
        ''' Calculates received interference from the others BS '''
        rx_inter = 0
        if (self.connected):
            for site in sites:
                for cell in site.cells:
                    if (self.cell_id != cell.id and self.cell_fr == cell.fr):
                        rx_watts = utl.dbm2watts(self.received_power(site, cell.id, tti))
                        rx_inter += rx_watts
        else:
            logger.error("UE don't connnected to one BS")
        return utl.watts2dbm(rx_inter)

    def sinr(self, sites, tti):
        ''' Calculates Signal-to-Interference-plus-Noise Ratio (SINR) level '''
        if (self.connected):
            r_pwr = self.received_power_connected(sites, tti)
            i_pwr = self.received_interference(sites, tti)
            
            n_pwr = sites

        else:
            logger.error("UE don't connnected to one BS")
        return utl.watts2dbm(rx_inter)

    def best_cell(self, sites, tti):
        ''' Return id of Cell with the best power '''
        best_site = sites[0]
        best_cell = best_site.cells[0]
        for site in sites:
            for cell in site.cells:
                if (self.received_power(site, cell.id, tti) > self.received_power(best_site, best_cell.id, tti)):
                    best_site = site
                    best_cell = cell
        return best_cell.id
     
    def connect_to_cell(self, cell):
        ''' Connect UE to Cell with cell_id '''        
        self.cell_id = cell.id
        self.cell_fr = cell.fr
        self.connected = True