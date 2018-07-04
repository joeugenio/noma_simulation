#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 28/06/2018
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
import cProfile as profile

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

    # throughput performance for N0MA
    thr_search = []
    thr_fair = []
    thr_random = []
    thr_fix = []
    
    # exhaustive search
    pairs1 = uppa.uppa(ues_uppa, cell, up_mode='search', pa_mode='fair', thr_func=perf.throughput_noma)
    for p  in pairs1:
        thr_search.append(perf.throughput_noma(p.users, bw_sb=cell.bw_sb))
    # average user throughput
    thr_user_search = np.mean(thr_search)
    # sum cell throughput
    thr_cell_search = np.sum(thr_search)
    # throughout sum per subband
    thr_sub_search = np.mean([np.sum(p) for p in thr_search])
    # array
    athr_search = np.array(thr_search)
    # throughput for each user in pair (R1 and R2)
    thr_r1_search = athr_search[:,0].mean()
    thr_r2_search = athr_search[:,1].mean()

    # fair user pair
    pairs2 = uppa.uppa(ues_uppa, cell, up_mode='fair', pa_mode='fair')
    for p  in pairs2:
        thr_fair.append(perf.throughput_noma(p.users, bw_sb=cell.bw_sb))
    # average user throughput
    thr_user_fair = np.mean(thr_fair)
    # sum cell throughput
    thr_cell_fair = np.sum(thr_fair)
    # throughout sum per subband
    thr_sub_fair = np.mean([np.sum(p) for p in thr_fair])
    # array
    athr_fair = np.array(thr_fair)
    # throughput for each user in pair (R1 and R2)
    thr_r1_fair = athr_fair[:,0].mean()
    thr_r2_fair = athr_fair[:,1].mean()

    # random user pair
    pairs3 = uppa.uppa(ues_uppa, cell, up_mode='random', pa_mode='fair')
    for p  in pairs3:
        thr_random.append(perf.throughput_noma(p.users, bw_sb=cell.bw_sb))
    # average user throughput
    thr_user_random = np.mean(thr_random)
    # sum cell throughput
    thr_cell_random = np.sum(thr_random)
    # throughout sum per subband
    thr_sub_random = np.mean([np.sum(p) for p in thr_random])
    # array
    athr_random = np.array(thr_random)
    # throughput for each user in pair (R1 and R2)
    thr_r1_random = athr_random[:,0].mean()
    thr_r2_random = athr_random[:,1].mean()
 
    # fair user pair and fix power allocation
    pairs4 = uppa.uppa(ues_uppa, cell, up_mode='fair', pa_mode='fix')
    for p  in pairs4:
        thr_fix.append(perf.throughput_noma(p.users, bw_sb=cell.bw_sb))
    # average user throughput
    thr_user_fix = np.mean(thr_fix)
    # sum cell throughput
    thr_cell_fix = np.sum(thr_fix)
    # throughout sum per subband
    thr_sub_fix = np.mean([np.sum(p) for p in thr_fix])
    # array
    athr_fix = np.array(thr_random)
    # throughput for each user in pair (R1 and R2)
    thr_r1_fix = athr_fix[:,0].mean()
    thr_r2_fix = athr_fix[:,1].mean()
    
    return [0]
        
      

    # r_noma = [thr_user_noma, thr_cell_noma, thr_sub_noma, thr_r1_noma, thr_r2_noma]
    # r_oma = [thr_user_oma, thr_cell_oma, thr_sub_oma, thr_r1_oma, thr_r2_oma]
    # # return r_noma and r_oma concatanate
    # return r_noma + r_oma

# create simulation
#s = sim.Simulator(n_ue_cell=10, coeff_pwr=0.8, coeff_bw=0.8, thr_target=80e6, n_cdf_arg=2, filename=file_name)
s = sim.Simulator(n_ue_cell=6, n_snap=1, filename=file_name)
# create scenario
s.scenario_generator()
# create statistics
stats = []
for i in range(1):
    stats.append(perf.Statistics(thr_target=80e6))
# run simulator
s.run(my_drop, stats)

# profile.run("s.run(my_drop, stats)")
