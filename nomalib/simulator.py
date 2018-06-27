#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 07/05/2018
# Version: 0.1

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
    def __init__(self, sim, tti=const.TTI, t_snap=const.T_SNP):
        self.t_snap = t_snap
        self.n_tti = int(t_snap/tti)
        self.grid = sim.grid
        try:
            self.n_ue_cell = sim.n_ue_cell
        except AttributeError:
            self.n_ue_cell = const.N_UE_CELL
        self.n_sites = len(self.grid.sites)
        self.n_cell_site = len(self.grid.sites[0].cells)
        self.n_cells = self.n_sites*self.n_cell_site
        self.sim = sim
        
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
        # pairs = uppa.user_pair(ue_sinr, n_sb=cell.n_sb, n_ma_ue=cell.n_ma_ue, mode='fair')
        
        # throughput performance for N0MA
        # thr_user_avg_noma = []
        # thr_cell_sum_noma = []
        # thr_r1r2_noma = []

        # throughput performance for OMA
        # thr_user_avg_oma = []
        # thr_cell_sum_oma = []
        # thr_r1r2_oma = []

        # for p in pairs:
            # Power and band allocation
            # uppa.power_allocation(p, alpha=self.sim.coeff_pwr, mode='fair')
            # Throughput NOMA
            # t_noma = perf.throughput_noma(p, cell.bw_sb)
            # average user throughput per subband
            # thr_user_avg_noma.append(np.mean(t_noma))
            # throughout sum per subband
            # thr_cell_sum_noma.append(np.sum(t_noma))
            # throughput for each user in pair (R1 and R2)
            # thr_r1r2_noma.append(t_noma)

            # Power and band allocation
            # uppa.band_allocation(p, beta=self.sim.coeff_bw, mode='fair')
            # Throughput OMA
            # t_oma = perf.throughput_oma(p, cell.bw_sb)
            # average user throughput per subband
            # thr_user_avg_oma.append(np.mean(t_oma))
            # throughout sum per subband
            # thr_cell_sum_oma.append(np.sum(t_oma))
            # throughput for each user in pair (R1 and R2)
            # thr_r1r2_oma.append(t_oma)
            

        # NOMA - average user, subband ecell throughout        
        # thr_user_noma = np.mean(thr_user_avg_noma)
        # thr_cell_noma = np.sum(thr_cell_sum_noma)
        # thr_sbb_noma = np.mean(thr_cell_sum_noma)
        # r_noma = [thr_user_noma, thr_cell_noma, thr_sbb_noma]
        # r_noma = [thr_user_noma]
        # average user throughput in same subband
        # r1_avg_noma = np.array(thr_r1r2_noma)[:,0].mean()
        # r2_avg_noma = np.array(thr_r1r2_noma)[:,1].mean()
        # r_noma = [r1_avg_noma, r2_avg_noma]
        
        # OMA - average user, subband ecell throughout
        # thr_user_oma = np.mean(thr_user_avg_oma)
        # thr_cell_oma = np.sum(thr_cell_sum_oma)
        # thr_sbb_oma = np.mean(thr_cell_sum_oma)
        # r_oma = [thr_user_oma, thr_cell_oma, thr_sbb_oma]
        # r_oma = [thr_user_oma]
        # r1_avg_oma = np.array(thr_r1r2_oma)[:,0].mean()
        # r2_avg_oma = np.array(thr_r1r2_oma)[:,1].mean()
        # r_oma = [r1_avg_oma, r2_avg_oma]
        
        # logger.info('Disconnecting all UEs')
        self.grid.disconnect_all_ue()
        self.grid.remove_all_ue()

        # return r_noma, r_oma
        return 0, 10

class Simulator:
    ''' System Level Simulator Class ''' 
    def __init__(self, n_snap=const.N_SNP, **kwargs):
        self.n_snap = n_snap
        self.grid = None
        self.snapshot = None
        for key,value in kwargs.items():
            setattr(self, key, value)
    
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
        self.snapshot = Snapshot(self)
        t.toc()
       
    def run(self):
        logger.info('Running simulation')
        t.tic()
        prob_noma = perf.Probability(self)
        prob_oma = perf.Probability(self)
        # progress bar
        for i in tqdm(range(self.n_snap), miniters=20, unit=' snapshot'):
            r_noma, r_oma = self.snapshot.run()
            # prob_noma.get_cdf(r_noma)
            # prob_oma.get_cdf(r_oma)
        # normalizes CDF
        # prob_noma.cdf /= self.n_snap
        # prob_oma.cdf /= self.n_snap

        logger.info('Saving data file')
        try:
            file_desc = self.filename
        except AttributeError:
            file_desc = str(id(self))
        file1 = const.OUT_PATH+'noma_'+file_desc
        file2 = const.OUT_PATH+'oma_'+file_desc
        # np.save(file1, [prob_noma])
        # np.save(file2, [prob_oma])
        # logger.info('Files saved: ')
        logger.info(file1)
        logger.info(file2)
        logger.info('Parameters used in the simulation:')
        attr = self.__dict__.copy()
        attr.pop('grid')
        attr.pop('snapshot')
        for k,v in attr.items():
            logger.info(str(k)+': '+str(v))
        logger.info('Finished Simulation')
        t.toc()