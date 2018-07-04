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

class BestPair:
    ''' Class for search best pair for exahustive search '''
    def __init__(self):
        self.branch = []
        self.all_pairs = []

    def available_pairs(self, u):
        u.sort(key=lambda x: x.sinr.mean(), reverse=True)
        pairs = []
        k = 0
        n = len(u)
        for i in range(n):
            for j in range(1+i, n):
                pairs.append(Pair(k, u[i],u[j]))
                k += 1
        return pairs

    def all_branchs(self, users):
        pairs = self.available_pairs(users)
        for p in pairs:
            u = users.copy()
            self.branch.append(p)
            u.remove(p.u1)
            u.remove(p.u2)
            if u != []:
                self.all_branchs(u)
            else:
                self.all_pairs.append(self.branch.copy())
            self.branch.pop()
        return

    def search_best_pairs(self, users, thr_func, pa_mode='fair'):
        ues = users.copy()
        self.all_branchs(ues)
        thr_max = 0
        best_pairs = None
        for pairs in self.all_pairs:
            thr = []
            for p in pairs:
                power_allocation(p, mode=pa_mode)
                thr.append(thr_func(p.users, 1))
            thr_cell = np.sum(thr)
            if thr_cell > thr_max:
                thr_max = thr_cell
                best_pairs = pairs
        return best_pairs

# User pair function
def user_pair(ues_uppa, n_sb, n_ma_ue=const.N_MA_UE, mode='random', func=None):
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
        b = BestPair()
        pairs = b.search_best_pairs(ues_uppa, func, 'fair')
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
def uppa(ues, cell, up_mode='fair', pa_mode='fair', thr_func=None):
    pairs = user_pair(ues, n_sb=cell.n_sb, n_ma_ue=cell.n_ma_ue, mode=up_mode, func=thr_func)
    for p in pairs:
        # power allocation for NOMA analysis
        power_allocation(p, mode=pa_mode)
        # band allocation for OMA analysis
        band_allocation(p)
    return pairs