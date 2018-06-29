#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 29/06/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Case study with 2 users per cell

import nomalib.simulator as sim
import nomalib.uppa as uppa
import nomalib.performance as perf
import numpy as np
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
    pairs = uppa.uppa(ues_uppa, cell, up_mode='fair', pa_mode='fair')

    # throughput performance for N0MA
    thr_noma = []
    thr_oma = []

    for p in pairs:
        # Throughput NOMA for each user
        thr_noma.append(perf.throughput_noma(p.users, cell.bw_sb))
        thr_oma.append(perf.throughput_oma(p.users, cell.bw_sb))
        
    # average user throughput
    thr_user_noma = np.mean(thr_noma)
    thr_user_oma = np.mean(thr_oma)
    # sum cell throughput
    thr_cell_noma = np.sum(thr_noma)
    thr_cell_oma = np.sum(thr_oma)
    # throughout sum per subband
    thr_sub_noma = np.mean([np.sum(p) for p in thr_noma])
    thr_sub_oma = np.mean([np.sum(p) for p in thr_oma])
    athr_noma = np.array(thr_noma)
    athr_oma = np.array(thr_oma)
    # throughput for each user in pair (R1 and R2)
    thr_r1_noma = athr_noma[:,0].mean()
    thr_r2_noma = athr_noma[:,1].mean()
    thr_r1_oma = athr_oma[:,0].mean()
    thr_r2_oma = athr_oma[:,1].mean()
    r_noma = [thr_user_noma, thr_cell_noma, thr_sub_noma, thr_r1_noma, thr_r2_noma]
    r_oma = [thr_user_oma, thr_cell_oma, thr_sub_oma, thr_r1_oma, thr_r2_oma]
    # return r_noma and r_oma concatanate
    return r_noma + r_oma

# create simulation
#s = sim.Simulator(n_ue_cell=10, coeff_pwr=0.8, coeff_bw=0.8, thr_target=80e6, n_cdf_arg=2, filename=file_name)
s = sim.Simulator(n_ue_cell=10, filename=file_name)
# create scenario
s.scenario_generator()
# create statistics
stats = []
target = [8e6,70e6,16e6,12e6,6e6]*2
for i in range(10):
    stats.append(perf.Statistics(thr_target=target[i]))
# run simulator
s.run(my_drop, stats)
