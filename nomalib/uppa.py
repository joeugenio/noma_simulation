#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 05/05/2018
# Last update: 07/05/2018
# Version: 0.1

# User Pair and Power Allocation for NOMA communications simulations

import nomalib.constants as const
import numpy as np

class User:
    ''' User class for User Pair '''
    def __init__(self, id, sinr, noma=None, oma=None):
        self.id = id
        self.sinr = sinr
        self.power = noma
        self.band = oma

class Pair:
    ''' Pair class for UPPA'''
    def __init__(self, id, users):
        self.id = id
        self.users = users

# User pair function
def user_pair(ues_sinr, n_sb, n_ma_ue=const.N_MA_UE, mode='random'):
    ues = ues_sinr[:]
    pairs = []
    if mode == 'random':
        for n in range(n_sb):
            u = []
            # randon user pair
            for m in range(n_ma_ue):
                u.append(ues.pop(np.random.randint(len(ues))))
            # sort by SINR
            u.sort(key=lambda x: x.sinr.mean(), reverse=True)
            pairs.append(Pair(id=n, users=u))
    elif mode == 'max_gain':
        pass
    else:
        pass
    return pairs

# Power allocation function for NOMA (power domain)
def power_allocation(pair, alpha, mode='equal'):
    if mode == 'equal':
        n = len(pair.users)
        for u in pair.users:
            u.power = np.ones(len(u.sinr))*(1/n)
    elif mode == 'fair':
        u1 = pair.users[0]
        u2 = pair.users[1]        
        u1.power = np.ones(len(u1.sinr))*(alpha)
        u2.power = np.ones(len(u2.sinr))*(1-alpha)

# Power allocation function for OMA (frequency domain)
def band_allocation(pair, beta, mode='equal'):
    if mode == 'equal':
        n = len(pair.users)        
        for u in pair.users:
            u.band = np.ones(len(u.sinr))*(1/n)
    elif mode == 'fair':
        u1 = pair.users[0]
        u2 = pair.users[1]        
        u1.band = np.ones(len(u1.sinr))*(beta)
        u2.band = np.ones(len(u2.sinr))*(1-beta)