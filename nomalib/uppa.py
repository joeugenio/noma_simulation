#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 05/05/2018
# Last update: 27/06/2018
# Version: 0.1

# User Pair and Power Allocation for NOMA communications simulations

import nomalib.constants as const
import numpy as np

class User:
    ''' User class for User Pair '''
    def __init__(self, id, sinr, pwr_coef=None, bnd_coef=None):
        self.id = id
        self.sinr = sinr
        self.pwr_coef = pwr_coef
        self.bnd_coef = bnd_coef

class Pair:
    ''' User Pair class for UPPA'''
    def __init__(self, id, u1, u2):
        self.id = id
        self.u1 = u1
        self.u2 = u2
        self.users = [u1, u2]

# User pair function
def user_pair(ues_uppa, n_sb, n_ma_ue=const.N_MA_UE, mode='random'):
    ues = ues_uppa[:]
    pairs = []
    if mode == 'random':
        for n in range(n_sb):
            u = []
            # randon user pair
            for m in range(n_ma_ue):
                u.append(ues.pop(np.random.randint(len(ues))))
            # sort by SINR
            u.sort(key=lambda x: x.sinr.mean(), reverse=True)
            pairs.append(Pair(id=n, u1=u[0], u2=u[1]))
    elif mode == 'fair':
        # sort users by SINR
        ues.sort(key=lambda x: x.sinr.mean())
        for s in range(n_sb):
            u1 = ues[s+n_sb]
            u2 = ues[s]
            pairs.append(Pair(id=s, u1=u1, u2=u2))
    elif mode == 'search':
        pass
    return pairs

# Power allocation function for NOMA (power domain)
def power_allocation(pair, alpha=0.2, mode='fix'):
    if mode == 'equal':
        n = len(pair.users)
        for u in pair.users:
            u.pwr_coef = 1/n
    elif mode == 'fix':
        pair.u1.pwr_coef = alpha
        pair.u2.pwr_coef = (1-alpha)
    elif mode == 'fair':
        sinr2 = pair.u2.sinr.mean()
        alpha = (np.sqrt(1+sinr2)-1)/sinr2
        pair.u1.pwr_coef = alpha
        pair.u2.pwr_coef = 1-alpha

# Power allocation function for OMA (frequency domain)
def band_allocation(pair, beta=0.5, mode='equal'):
    if mode == 'equal':
        n = len(pair.users)
        for u in pair.users:
            u.bnd_coef = 1/n
    elif mode == 'fair':
        pair.u1.bnd_coef = beta
        pair.u2.bnd_coef = 1-beta

# Run User Pair and Power Allocation functions
def uppa(ues, cell, up_mode='fair', pa_mode='fair'):
    pairs = user_pair(ues, n_sb=cell.n_sb, n_ma_ue=cell.n_ma_ue, mode=up_mode)
    for p in pairs:
        # power allocation for NOMA analysis
        power_allocation(p, mode=pa_mode)
        # band allocation for OMA analysis
        band_allocation(p)
    return pairs