#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 26/03/2018
# Version: 1.0

# Performance evaluation Python Script for NOMA communications simulations

import nomalib.constants as const
import numpy as np

class Performance:
    ''' Performance class '''
    def __init__(self):
        self.sinr = []
        self.throughput_user = []
        self.throughput_cell = []
        self.throughput_cell_edge = []
        self.throughput_sum = []
        self.throughput_cdf = []

    def amc_lte(self, sinr_vector):
        thr = []
        for sinr in sinr_vector:
            if (sinr <= -9.478):
                rc = 0
                m = 2
            elif (-9.478 < sinr <= -6.658):
                rc = 78
                m = 2
            elif (-6.658 < sinr <= -4.098):
                rc = 120
                m = 2
            elif (-4.098 < sinr <= -1.798):
                rc = 193
                m = 2
            elif (-1.798 < sinr <= 0.399):
                rc = 308
                m = 2
            elif (0.399 < sinr <= 2.424):
                rc = 449
                m = 2
            elif (2.424 < sinr <= 4.489):
                rc = 602
                m = 2
            elif (4.489 < sinr <= 6.367):
                rc = 378
                m = 4
            elif (6.367 < sinr <= 8.456):
                rc = 490
                m = 4
            elif (8.456 < sinr <= 10.266):
                rc = 616
                m = 4
            elif (10.266 < sinr <= 12.218):
                rc = 466
                m = 6
            elif (12.218 < sinr <= 14.122):
                rc = 567
                m = 6
            elif (14.122 < sinr <= 15.849):
                rc = 666
                m = 6
            elif (15.849 < sinr <= 17.786):
                rc = 772
                m = 6
            elif (17.786 < sinr <= 19.809):
                rc = 873
                m = 6
            elif (19.809 < sinr):
                rc = 948
                m = 6
            thr.append(rc*m/1024)
        return np.array(thr)
    
    def shannon(self, sinr_vector, bw=const.SB):
        sinr_lin = 10**(sinr_vector/10)
        thr = bw*np.log2(1+sinr_lin)
        return thr
    
    def shannon_trunc(self, sinr_vector, bw=const.SB, r_max_norm = 948*6/1024):
        r_max = r_max_norm*bw        
        sinr_lin = 10**(sinr_vector/10)
        thr = bw*np.log2(1+sinr_lin)
        try:
            thr = np.array([t if t <= r_max else r_max for t in thr])
        except TypeError:
            thr = thr if thr <= r_max else r_max            
        return thr
    
    def shannon_att(self, sinr_vector, att=const.SHN_ATT, bw=const.SB, r_max_norm = 948*6/1024):
        r_max = r_max_norm*bw
        thr = att*self.shannon(sinr_vector, bw)
        try:
            thr = np.array([t if t <= r_max else r_max for t in thr])
        except TypeError:
            thr = thr if thr <= r_max else r_max
        return thr

    def throughput_oma(self, sinr, beta=1, bw=const.SB, model='shannon_att'):
        func = {'amc':self.amc_lte,
                'shannon':self.shannon,
                'shannon_trunc':self.shannon_trunc,
                'shannon_att':self.shannon_att}
        thr = func[model](sinr)
        return thr