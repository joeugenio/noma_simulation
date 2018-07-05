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

    # exhaustive search
    pairs1 = uppa.uppa(ues_uppa, cell, up_mode='search', pa_mode='fair', thr_func=perf.throughput_noma)
    # fair user pair
    pairs2 = uppa.uppa(ues_uppa, cell, up_mode='fair', pa_mode='fair')
    # random user pair
    pairs3 = uppa.uppa(ues_uppa, cell, up_mode='random', pa_mode='fair')
    # fair user pair and fix power allocation
    pairs4 = uppa.uppa(ues_uppa, cell, up_mode='fair', pa_mode='fix')

    cases = [pairs1, pairs2, pairs3, pairs4]
    user_thr = []
    cell_thr = []
    sub_thr = []
    user_jain = []
    pair_jain = []
    gain_jain = []
    # all uppa algoritms
    for case in cases:
        thr = []
        j = []
        for p  in case:
            t = perf.throughput_noma(p.users, bw_sb=cell.bw_sb)
            thr.append(t)
            # jain's index based on differece betwee multiple access and exclusive access rate
            t1 = perf.shannon_att(p.u1.sinr, bw=cell.bw_sb).mean()
            t2 = perf.shannon_att(p.u2.sinr, bw=cell.bw_sb).mean()
            j.append(t1-t[0])
            j.append(t2-t[1])
        # average user throughput
        user_thr.append(np.mean(thr))
        # sum cell throughput
        cell_thr.append(np.sum(thr))
        # throughout sum per subband
        sub_thr.append(np.mean([np.sum(p) for p in thr]))
        # jain's index for users
        user_jain.append(perf.jain(np.array(thr).reshape(-1)))
        # jain's index for subbands
        pair_jain.append(perf.jain(np.array([np.sum(p) for p in thr])))
        # jain's index for gain per user
        gain_jain.append(perf.jain(np.array(j)))
    
    # OMA case
    thr = []
    j = []
    for p in pairs2:
        t = perf.throughput_oma(p.users, bw_sb=cell.bw_sb)
        thr.append(t)
        # jain's index based on differece betwee multiple access and exclusive access rate
        t1 = perf.shannon_att(p.u1.sinr, bw=cell.bw_sb).mean()
        t2 = perf.shannon_att(p.u2.sinr, bw=cell.bw_sb).mean()
        j.append(t1-t[0])
        j.append(t2-t[1])
    # average user throughput
    user_thr.append(np.mean(thr))
    # sum cell throughput
    cell_thr.append(np.sum(thr))
    # throughout sum per subband
    sub_thr.append(np.mean([np.sum(p) for p in thr]))
    # jain's index for users
    user_jain.append(perf.jain(np.array(thr).reshape(-1)))
    # jain's index for subbands
    pair_jain.append(perf.jain(np.array([np.sum(p) for p in thr])))
    # jain's index for gain per user
    gain_jain.append(perf.jain(np.array(j)))

    r = []
    for i in range(5):
        r+=[user_thr[i], cell_thr[i], sub_thr[i], user_jain[i], pair_jain[i], gain_jain[i]]
    return r
        
# create simulation
#s = sim.Simulator(n_ue_cell=10, coeff_pwr=0.8, coeff_bw=0.8, thr_target=80e6, n_cdf_arg=2, filename=file_name)
s = sim.Simulator(n_ue_cell=2, filename=file_name)
# create scenario
s.scenario_generator()
# create statistics
stats = []
tgt = [40e6,80e6,80e6,1,1,1]*5 # 2 users
low = [0, 0, 0, .5, .5, .5]*5
# tgt = [20e6,80e6,40e6,1,1,1]*5 # 4 users
# tgt = [16e6,80e6,25e6,1,1,1]*5 # 6 users
# tgt = [10e6,80e6,20e6,1,1,1]*5 # 8 users
# tgt = [8e6,70e6,16e6,1,1,1]*5  # 10 users
# tgt = [4e6,70e6,8e6,1,1,1]*5   # 20 users
# tgt = [3e6,70e6,6e6,1,1,1]*5   # 30 users
for i in range(6*5):
    stats.append(perf.Statistics(target=tgt[i], low=low[i]))
# run simulator
s.run(my_drop, stats)
