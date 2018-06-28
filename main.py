#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 08/05/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Case study with 2 users per cell

import nomalib.simulator as sim
import nomalib.uppa as uppa
import nomalib.performance as perf
import logzero
from logzero import logger
import __main__ as main

# set file name for logs and outputs files
file_name = main.__file__[2:-3:]

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/'+file_name+'.log', mode='a', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# implement drop function
# actions performed for each snapshot
def my_drop(snap):
    # SINR for all users from ERB view point
    grid = snap.grid
    site = snap.site
    cell = snap.cell
    ues_uppa = []        
    for ue_id in cell.ue_ids:
        ue = grid.get_ue(ue_id)
        s = perf.sinr(ue, cell, site, grid)
        ues_uppa.append(uppa.User(ue.id, s))
        
    # UPPA from fair method
    pairs = uppa.uppa(ues_uppa, cell, mode='fair')
    for p in pairs:
        thr = perf.throughput_oma(p, cell.bw_sb)
        print(thr)
        
    # throughput performance for N0MA
    # thr_user_noma = []
    # thr_cell_noma = []
    # thr_sub_noma = []
    # thr_r1_noma = []
    # thr_r2_noma = []


    # Throughput NOMA
    # t_noma = perf.throughput_noma(p, cell.bw_sb)
    # average user throughput per subband
    # thr_user_avg_noma.append(np.mean(t_noma))
    # throughout sum per subband
    # thr_cell_sum_noma.append(np.sum(t_noma))
    # throughput for each user in pair (R1 and R2)
    # thr_r1r2_noma.append(t_noma)
           

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

# 
       

# create simulation
#s = sim.Simulator(n_ue_cell=10, coeff_pwr=0.8, coeff_bw=0.8, thr_target=80e6, n_cdf_arg=2, filename=file_name)
s = sim.Simulator(n_ue_cell=10, n_snap=2, filename=file_name)
# create scenario
s.scenario_generator()
# run simulator
s.run(drop=my_drop)