#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 25/03/2018
# Version: 1.0

# Simulator Python Script for NOMA communications simulations

import nomalib.constants as const
import nomalib.utils as utl
import nomalib.network as net
import nomalib.channel as ch
from logzero import logger
from pytictoc import TicToc
import numpy as np

t = TicToc()
class Snapshot:
    ''' Snapshot Class '''
    def __init__(self, tti=const.TTI, t_snap=const.T_SNP, mode=const.MOD):
        self.t_snap = t_snap
        self.n_tti = int(t_snap/tti)
        self.mode = mode
        # all cells and all sites
        if (self.mode == 'grid'):
            self.sites = range(const.N_BS)
            self.cells = range(const.N_SEC)
        # all cells in sites[9]
        elif (self.mode == 'site'):
            self.sites = range(9,10)
            self.cells = range(const.N_SEC)
        # cells[0] in sites[9]
        elif (self.mode == 'cell'):
            self.sites = range(9,10)
            self.cells = range(1)
        else:
            logger.error('Invalid mode (grid, site, cell)')
        
    def run(self, grid):
        h = ch.TemporalChannel().h
        # logger.info('Deploing users equipments on grid')
        grid.deploy_user_equipment(region='hexagon')
        # logger.info('Connecting UE to best BS')
        grid.connect_all_ue()
        u = 0
        grid_sinr = []
        for s in self.sites:
            site_sinr = []
            for c in self.cells:
                cell_sinr = []
                for ue_id in grid.sites[s].cells[c].ue_ids:
                    ue = grid.get_ue(ue_id)
                    r_pwr = ue.received_power_connected(grid.sites)
                    r_inter = ue.received_interference(grid.sites)
                    sinr = []
                    for t in range(self.n_tti):
                        p = utl.dbm2watts(r_pwr + h[u][0].gain[t])
                        i = 0
                        for j in range(len(r_inter)):
                            i += utl.dbm2watts(r_inter[j] + h[u][j+1].gain[t])
                        sinr.append(p/i)
                    u += 1
                    cell_sinr.append(sinr)
                site_sinr.append(cell_sinr)
            grid_sinr.append(site_sinr)
        # logger.info('Disconnecting all UEs')
        grid.disconnect_all_ue()
        return grid_sinr

class Simulator:
    ''' System Level Simulator Class '''
    def __init__(self, n_snap=const.N_SNP, mode=const.MOD):
        self.n_snap = n_snap
        self.mode = mode
        self.grid = None
        self.snapshot = Snapshot(mode=mode)

    def scenario_generator(self):
        t.tic()        
        ''' Generates mobile communication scenario '''
        logger.info('Creating grid with 19 sites')
        self.grid = net.Grid()
        logger.info('Deploing base stations on grid')
        self.grid.deploy_base_station()
        logger.info('Starting all base stations')
        self.grid.start_all_base_stations()
        t.toc()
        
    def run(self):
        logger.info('Runing simulation')
        t.tic()
        sinr = []
        for i in range(self.n_snap):
            r = self.snapshot.run(self.grid)
            sinr.append(r)
            if (i % 100 == 0):
                logger.info(str(i)+' snapshots completed')
        np.save(const.OUT_PATH+'sinr0', sinr)
        t.toc()