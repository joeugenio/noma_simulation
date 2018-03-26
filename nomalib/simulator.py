#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 25/03/2018
# Version: 1.0

# Simulator Python Script for NOMA communications simulations

import nomalib.network as net
import nomalib.utils as utl
import nomalib.constants as const
import logzero
from logzero import logger
import numpy as np

class Simulator:
    ''' System Level Simulator Class '''
    def __init__(self, tti=const.TTI, n_snap=const.N_SNP, t_snap=const.T_SNP):
        self.n = n_snap
        self.t = t_snap
        self.n_tti = int(t_snap/tti)

    def scenario_generator(self):
        ''' Generates mobile communication scenario '''
        logger.info('Creating grid with 19 sites')
        grid = net.Grid()
        logger.info('Deploing base stations on grid')
        grid.deploy_base_station()
        logger.info('Deploing users equipments on grid')
        grid.deploy_user_equipment(region='hexagon')
        logger.info('Starting all base stations')
        grid.start_all_base_stations()
        # logger.info('Connecting UE to best BS')
        # grid.connect_all_ue()
    
    def run_snapshot(self):
        for i in range(self.n_tti):
            