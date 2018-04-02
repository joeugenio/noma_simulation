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
from logzero import logger
from pytictoc import TicToc
import numpy as np

t = TicToc()
class Simulator:
    ''' System Level Simulator Class '''
    def __init__(self, n_snap=const.N_SNP, mode='grid'):
        self.n_snap = n_snap
        self.mode = mode
        self.grid = None

    def scenario_generator(self):
        t.tic()        
        ''' Generates mobile communication scenario '''
        logger.info('Creating grid with 19 sites')
        self.grid = net.Grid()
        logger.info('Deploing base stations on grid')
        self.grid.deploy_base_station()
        logger.info('Starting all base stations')
        self.grid.start_all_base_stations()

        logger.info('Deploing users equipments on grid')
        self.grid.deploy_user_equipment(region='hexagon')
        logger.info('Connecting UE to best BS')
        self.grid.connect_all_ue()
        t.toc()
        
    def run(self):
        t.tic()
        for i in range(self.n_snap):
            pass
            # self.run_snapshot()
        t.toc()
    
class Snapshot:
    ''' Snapshot Class '''
    def __init__(self, tti=const.TTI, n_snap=const.N_SNP, t_snap=const.T_SNP, mode='grid'):
        self.n_snap = n_snap
        self.t_snap = t_snap
        self.n_tti = int(t_snap/tti)
        self.mode = mode

    def run_snapshot(self, grid):
        logger.info('Deploing users equipments on grid')
        grid.deploy_user_equipment(region='hexagon')
        logger.info('Connecting UE to best BS')
        grid.connect_all_ue()
        if (self.mode == 'grid'):
            pass
        elif (self.mode == 'site'):
            pass
        elif (self.mode == 'cell'):
            pass
        else:
            logger.error('Invalid mode (grid, site, cell)')
        # sites = self.grid.sites
        # ues = self.grid.user_equipments
        # sinr = []
        # for ue in ues:
        #     time = []
        #     for tti in range(self.n_tti):
        #         time.append(ue.sinr(sites, tti))
        #     sinr.append(time)
        self.grid = None