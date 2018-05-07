#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 25/03/2018
# Last update: 07/05/2018
# Version: 0.1

# Performance evaluation Python functios for NOMA communications simulations

import nomalib.constants as const
import nomalib.channel as ch
import nomalib.utils as utl
import numpy as np

def sinr(ue, cell, site, grid):
    h = ch.SmallScaleEffect(size=len(grid.sites)).h
    # power
    rx_pwr = utl.dbm2watts(ue.received_power_connected(grid.sites))
    p_sb = rx_pwr*h[0].gain
    rx_inter = utl.dbm2watts(ue.received_interference(grid.sites))
    # interference
    i_sb = np.zeros(len(p_sb))
    for k in range(len(rx_inter)):
        i_sb += rx_inter[k]*h[k+1].gain
    # noise
    n_sb = utl.dbm2watts(site.noise.floor)/cell.n_sb
    # SINR per subband
    sinr_sb = p_sb/(i_sb + n_sb)
    return sinr_sb


def amc_lte(sinr_vector):
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

def shannon(sinr, bw=1, scale='lin'):
    if scale=='db':
        sinr = 10**(sinr/10)
    thr = bw*np.log2(1+sinr)
    return thr

def shannon_trunc(sinr, bw=1, r_max_norm = 948*6/1024, scale='lin'):
    r_max = r_max_norm*bw 
    if scale=='db':
        sinr = 10**(sinr/10)
    thr = bw*np.log2(1+sinr)
    try:
        thr = np.array([t if t <= r_max else r_max for t in thr])
    except TypeError:
        thr = thr if thr <= r_max else r_max            
    return thr

def shannon_att(sinr, bw=1, att=const.SHN_ATT, r_max_norm = 948*6/1024, scale='lin'):
    r_max = r_max_norm*bw
    thr = att*shannon(sinr, bw, scale=scale)
    try:
        thr = np.array([t if t <= r_max else r_max for t in thr])
    except TypeError:
        thr = thr if thr <= r_max else r_max
    return thr

def throughput_oma(pair, bw_sb=1, model='shannon_att'):
    n_ue = len(pair.users)
    pwr = 1/n_ue
    func = {'amc':amc_lte,
            'shannon':shannon,
            'shannon_trunc':shannon_trunc,
            'shannon_att':shannon_att}
    thr = []    
    for u in pair.users:
        sinr = u.sinr
        beta = u.band
        t = beta*func[model](sinr*(pwr/beta), bw=bw_sb)
        thr.append(t.mean())
    return thr
    
def throughput_noma(pair, bw_sb=1, model='shannon_att'):
    func = {'amc':amc_lte,
            'shannon':shannon,
            'shannon_trunc':shannon_trunc,
            'shannon_att':shannon_att}
    thr = []
    a = np.zeros(len(pair.users[0].power))
    for u in pair.users:
        sinr = u.sinr
        alpha = u.power
        num = alpha*sinr
        den = a*sinr + 1
        t = func[model]((num/den), bw=bw_sb)
        thr.append(t.mean())
        a += alpha
    return thr

class Probability:
    def __init__(self, max=70e6, len_arg=3, size=100):
        self.size = size
        self.max = max
        self.thr = np.linspace(0, max, size)
        self.cdf = np.zeros((len_arg, size))
        self.len_arg = len_arg
    
    def get_cdf(self, value):
        for i in range(self.size):
            for j in range(self.len_arg):
                if value[j] <= self.thr[i]:
                    self.cdf[j][i] += 1 