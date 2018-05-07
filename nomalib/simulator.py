#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 07/05/2018
# Version: 1.0

# Simulator Python Script for NOMA communications simulations

import nomalib.constants as const
import nomalib.network as net
import nomalib.uppa as uppa
import nomalib.performance as perf
import numpy as np
from logzero import logger
from tqdm import tqdm
from pytictoc import TicToc

t = TicToc()
class Snapshot:
    ''' Snapshot Class '''
    def __init__(self, grid, tti=const.TTI, t_snap=const.T_SNP, n_ue_cell=const.N_UE_CELL):
        self.t_snap = t_snap
        self.n_tti = int(t_snap/tti)
        self.grid = grid
        self.n_ue_cell = n_ue_cell
        self.n_sites = len(grid.sites)
        self.n_cell_site = len(grid.sites[0].cells)
        self.n_cells = self.n_sites*self.n_cell_site
        
    def run(self):
        # Deploing users equipments on grid
        self.grid.deploy_user_equipments(n_ue=self.n_cells*self.n_ue_cell)
        # Connecting UE to best BS
        self.grid.connect_all_ue(n_ue=self.n_ue_cell)
        # Reserve power and subbands from number of uses connected'
        self.grid.resource_reserve_all()
        # Randomly chooses a site
        i_site = np.random.randint(self.n_sites)
        site = self.grid.sites[i_site]
        # Randomly chooses a cell
        i_cell = np.random.randint(self.n_cell_site)
        cell = site.cells[i_cell]

        # SINR for all users
        ue_sinr = []        
        for ue_id in cell.ue_ids:
            ue = self.grid.get_ue(ue_id)
            s = perf.sinr(ue, cell, site, self.grid)
            ue_sinr.append(uppa.User(ue.id, s))

        # UPPA from SINR values
        pairs = uppa.user_pair(ue_sinr, n_sb=cell.n_sb, n_ma_ue=cell.n_ma_ue)
        
        # throughput performance for N0MA
        thr_user_avg_noma = []
        thr_cell_sum_noma = []

        # throughput performance for OMA
        thr_user_avg_oma = []
        thr_cell_sum_oma = []

        for p in pairs:
            # Power and band allocation
            uppa.power_allocation(p, mode='fair')
            # Throughput NOMA
            t_noma = perf.throughput_noma(p, cell.bw_sb)            
            # average user throughput per subband
            thr_user_avg_noma.append(np.mean(t_noma))
            # throughout sum per subband
            thr_cell_sum_noma.append(np.sum(t_noma))

            # Power and band allocation
            uppa.band_allocation(p)
            # Throughput OMA
            t_oma = perf.throughput_oma(p, cell.bw_sb)
            # average user throughput per subband
            thr_user_avg_oma.append(np.mean(t_oma))
            # throughout sum per subband
            thr_cell_sum_oma.append(np.sum(t_oma))

        # NOMA - average user, subband ecell throughout        
        thr_user_noma = np.mean(thr_user_avg_noma)
        thr_cell_noma = np.sum(thr_cell_sum_noma)
        thr_sbb_noma = np.mean(thr_cell_sum_noma)
        r_noma = [thr_user_noma, thr_cell_noma, thr_sbb_noma]
        
        # OMA - average user, subband ecell throughout
        thr_user_oma = np.mean(thr_user_avg_oma)
        thr_cell_oma = np.sum(thr_cell_sum_oma)
        thr_sbb_oma = np.mean(thr_cell_sum_oma)
        r_oma = [thr_user_oma, thr_cell_oma, thr_sbb_oma]
        
        # logger.info('Disconnecting all UEs')
        self.grid.disconnect_all_ue()
        self.grid.remove_all_ue()

        return r_noma, r_oma

class Simulator:
    ''' System Level Simulator Class ''' 
    def __init__(self, n_snap=const.N_SNP, n_ue_cell=const.N_UE_CELL):
        self.n_snap = n_snap
        self.n_ue_cell = n_ue_cell
        self.grid = None
        self.snapshot = None

    def scenario_generator(self):
        t.tic()
        ''' Generates mobile communication scenario '''
        logger.info('Creating grid with 19 sites')
        self.grid = net.Grid()
        logger.info('Deploing base stations on grid')
        self.grid.deploy_base_station()
        logger.info('Starting all base stations')
        self.grid.start_all_base_stations()
        logger.info('Create snapshot simulation')
        self.snapshot = Snapshot(self.grid, n_ue_cell=self.n_ue_cell)
        t.toc()
       
    def run(self):
        logger.info('Running simulation')
        t.tic()
        prob_noma = perf.Probability()
        prob_oma = perf.Probability()

        for i in tqdm(range(self.n_snap), miniters=20, unit=' snapshot'):
            r_noma, r_oma = self.snapshot.run()
            prob_noma.get_cdf(r_noma)
            prob_oma.get_cdf(r_oma)
        
        np.save(const.OUT_PATH+'noma'+str(self.n_ue_cell), [prob_noma])
        np.save(const.OUT_PATH+'oma'+str(self.n_ue_cell), [prob_oma])

        logger.info('Finished Simulation')
        t.toc()