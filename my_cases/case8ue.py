#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 10/07/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Case study with 2 users per cell

import nomalib.simulator as sim
import nomalib.uppa as uppa
import nomalib.performance as perf
import numpy as np
import logzero
from logzero import logger

# set file name for logs and outputs files
file_name = __file__[2:-3:]
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
    ues_uppa1 = []        
    ues_uppa2 = []        
    ues_uppa3 = []        
    ues_uppa4 = []        
    for ue_id in cell.ue_ids:
        ue = grid.get_ue(ue_id)
        s = perf.sinr(ue, cell, site, grid)
        ues_uppa1.append(uppa.User(ue.id, s))
        ues_uppa2.append(uppa.User(ue.id, s))
        ues_uppa3.append(uppa.User(ue.id, s))
        ues_uppa4.append(uppa.User(ue.id, s))

    # exhaustive search
    pairs1 = uppa.uppa(ues_uppa1, cell, up_mode='search', pa_mode='fair', thr_func=perf.throughput_noma)
    # fair user pair
    pairs2 = uppa.uppa(ues_uppa2, cell, up_mode='fair', pa_mode='fair')
    # random user pair
    pairs3 = uppa.uppa(ues_uppa3, cell, up_mode='random', pa_mode='fair')
    # fair user pair and fix power allocation
    pairs4 = uppa.uppa(ues_uppa4, cell, up_mode='fair', pa_mode='fix')

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
    for i in range(4):
        r+=[user_thr[i], cell_thr[i], sub_thr[i], user_jain[i], pair_jain[i], gain_jain[i]]
    return r

def main():
    # define user number
    N = 8
    # create simulation
    s = sim.Simulator(n_ue_cell=N, filename=file_name)
    # create scenario
    s.scenario_generator()
    # create dictionary with highest values for CDF statistics calculator
    # dic = {users_numbers, list_of_high_values_for_cdf}
    values_max = {2:[40e6,80e6,80e6,1,1,1], 4:[20e6,80e6,40e6,1,1,1],
    6:[16e6,80e6,25e6,1,1,1], 8:[10e6,80e6,20e6,1,1,1],
    10:[8e6,70e6,16e6,1,1,1], 20:[4e6,70e6,8e6,1,1,1],
    30:[3e6,70e6,6e6,1,1,1]}
    # mapping number of users to highest values
    v_max = values_max[N]*4
    # run simulator
    s.run(my_drop, v_max)

if __name__ == '__main__':
    main()