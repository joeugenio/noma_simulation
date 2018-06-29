#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 28/06/2018
# Version: 0.1

# Simulator Python Script for NOMA communications simulations

import nomalib.constants as const
import nomalib.network as net
import numpy as np
from tqdm import tqdm
from logzero import logger
from pytictoc import TicToc

t = TicToc()
class Snapshot:
    ''' Snapshot Class '''
    def __init__(self, sim, tti=const.TTI, t_snap=const.T_SNP):
        self.t_snap = t_snap
        self.n_tti = int(t_snap/tti)
        self.grid = sim.grid
        self.site = None
        self.cell = None
        try:
            self.n_ue_cell = sim.n_ue_cell
        except AttributeError:
            self.n_ue_cell = const.N_UE_CELL
        self.n_sites = len(self.grid.sites)
        self.n_cell_site = len(self.grid.sites[0].cells)
        self.n_cells = self.n_sites*self.n_cell_site
        self.sim = sim
        
    def run(self, drop):
        # Deploing users equipments on grid
        self.grid.deploy_user_equipments(n_ue=self.n_cells*self.n_ue_cell)
        # Connecting UE to best BS
        self.grid.connect_all_ue(n_ue=self.n_ue_cell)
        # Reserve power and subbands from number of uses connected'
        self.grid.resource_reserve_all()
        # Randomly chooses a site
        i_site = np.random.randint(self.n_sites)
        self.site = self.grid.sites[i_site]
        # Randomly chooses a cell
        i_cell = np.random.randint(self.n_cell_site)
        self.cell = self.site.cells[i_cell]
        # Run a customized drop
        result = drop(self)
        # disconnect all users of cell
        self.grid.disconnect_all_ue()
        # remove all users of cell
        self.grid.remove_all_ue()
        # return result of snapshot
        return result

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
       
    def run(self, drop, stats):
        t.tic()
        # logger in formation about simulation
        logger.info('Parameters used in the simulation:')
        attr = self.__dict__.copy()
        attr.pop('grid')
        attr.pop('snapshot')
        for k,v in attr.items():
            logger.info(str(k)+': '+str(v))
        # running simulation drops
        logger.info('Running simulation')
        # progress bar
        for i in tqdm(range(self.n_snap), miniters=20, unit=' snapshot'):
            results = self.snapshot.run(drop)
            for r in range(len(results)):
                stats[r].cdf_calc(results[r])
        # normalizes CDF
        for s in stats:
            s.cdf /= self.n_snap 
        logger.info('Saving data file')
        try:
            file_desc = self.filename
        except AttributeError:
            file_desc = str(id(self))
        filename = const.OUT_PATH+'simul_'+file_desc
        np.save(filename, stats)
        logger.info('File saved:')
        logger.info(filename)
        logger.info('Finished Simulation')
        t.toc()