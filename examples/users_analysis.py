#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 08/05/2018
# Last update: 16/07/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Analysis from simulation results data

import nomalib.plots as plt
import nomalib.constants as const
import logzero
from logzero import logger
import __main__ as main
import numpy as np

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/'+main.__file__[2:-3:]+'.log', mode='a', loglevel=logzero.logging.DEBUG)
logger.info('Data analysis from simulation results')

logger.info('Load data from files')
case02 = np.load(const.OUT_PATH+'simul_case2ue.npy')
case04 = np.load(const.OUT_PATH+'simul_case4ue.npy')
case06 = np.load(const.OUT_PATH+'simul_case6ue.npy')
case08 = np.load(const.OUT_PATH+'simul_case8ue.npy')
case10 = np.load(const.OUT_PATH+'simul_case10ue.npy')
case20 = np.load(const.OUT_PATH+'simul_case20ue.npy')
case30 = np.load(const.OUT_PATH+'simul_case30ue.npy')

logger.info('Plot graphs: Throughout')
#==============================================================================
# get cell edge user throughput (cdf = 0.05)
#==============================================================================
def edge_user_indicators(stats, cdf=0.05):
    for i in range(len(stats.cdf)):
        if stats.cdf[i] >= cdf:
            prev = stats.cdf[i-1]
            curr = stats.cdf[i]
            diff_prev = abs(cdf - prev)
            diff_curr = abs(curr - cdf)
            if (diff_prev < diff_curr):
                thr = stats.rndv[i-1]
            else:
                thr = stats.rndv[i]
            return thr
#==============================================================================
# get user, pairs or cell average throughput
#==============================================================================
# calculate a PDF approximation based on CDF difference
def cdf2pdf(cdf):
    df = np.diff(cdf)
    df = np.insert(df, 0, df[0])
    return df
# calculate meand with pdf
def mean(x, pdf):
    return (x*pdf).sum()
# get a average values
# the threshold parameter is been used just
# for keep compatibility with edge_inicators method
def cdf2mean(stats, threshold=None):
    pdf = cdf2pdf(stats.cdf)
    return mean(stats.rndv, pdf)
#==============================================================================
# get all curves with users numbers variation
#==============================================================================
def get_curves(cases, n_users, n_curves,  _type, func, threshold):
    curves = []
    # n_cases = len(n_users)
    for c in range(n_curves):
        if c == 0:
            x = n_users[:3:]
            u_cases = cases[:3:]
        else:
            x = n_users
            u_cases = cases
        y = []
        for u in u_cases:
            nc = c if (len(u)==n_curves*6) else (c-1)
            s = u[nc*6+_type]
            m = func(s, threshold)
            y.append(m)
        curves.append((np.array(x), np.array(y)))
    return curves
#==============================================================================
# plot all graphs with users numbers variation
#==============================================================================
graph_type = {'user':0, 'cell':1, 'subband':2, 'jain_user':3, 'jain_pair':4, 'jain_gain':5}
cases = [case02, case04, case06, case08, case10, case20, case30]
n_users = [2,4,6,8,10,20,30]
n_curves = 5
#==============================================================================
#            NOMA vs OMA
#==============================================================================
# -----------------------------------------
#           Graph 1
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'noma_vs_oma/noma_vs_oma_cell_edge_user'
# # pairs
# # _type = graph_type['subband']
# # fn = 'noma_vs_oma/noma_vs_oma_cell_edge_pair'
# # cell
# # _type = graph_type['cell']
# # fn = 'noma_vs_oma/noma_vs_oma_cell_edge_cell'
# func = edge_user_indicators
# threshold = 0.05
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['NOMA', 'OMA']
# xsc = 1e6
# loc = 'lower right'
# -----------------------------------------
#           Graph 2
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'noma_vs_oma/noma_vs_oma_nearest_user'
# # pairs
# # _type = graph_type['subband']
# # fn = 'noma_vs_oma/noma_vs_oma_nearest_pair'
# # cell
# # _type = graph_type['cell']
# # fn = 'noma_vs_oma/noma_vs_oma_nearest_cell'
# func = edge_user_indicators
# threshold = 0.95
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['NOMA', 'OMA']
# xsc = 1e6
# loc = 'upper right'
# -----------------------------------------
#           Graph 3
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'noma_vs_oma/noma_vs_oma_mean_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'noma_vs_oma/noma_vs_oma_mean_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'noma_vs_oma/noma_vs_oma_mean_cell'
# # loc = 'lower right'
# func = cdf2mean
# threshold = 0.95
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['NOMA', 'OMA']
# xsc = 1e6
# -----------------------------------------
#           Graph 4
# -----------------------------------------
# Jain's index
# _type = graph_type['jain_gain']
# fn = 'noma_vs_oma/noma_vs_oma_jain_cell'
# loc = 'upper right'
# func = cdf2mean
# threshold = 0.95
# ylab = 'Índice de justiça de Jain'
# xlab = 'Número de EU'
# label = ['NOMA', 'OMA']
# xsc = 1
# curves =  get_curves(cases, n_users, n_curves, _type, func, threshold)
# plt.plot_uppa([curves[1], curves[4]], save=True, filename=fn, lab=label, ylab=ylab, xlab=xlab, xscale=xsc, lpos=loc)
#==============================================================================
#            Pairing
#==============================================================================
# -----------------------------------------
#           Graph 1
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'pairing/pairing_cell_edge_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'pairing/pairing_cell_edge_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'pairing/pairing_cell_edge_cell'
# # loc = 'lower right'
# func = edge_user_indicators
# threshold = 0.05
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['Ótimo', 'Justo', 'Aleatório']
# xsc = 1e6
# -----------------------------------------
#           Graph 2
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'pairing/pairing_nearest_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'pairing/pairing_nearest_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'pairing/pairing_nearest_cell'
# # loc = 'upper right'
# func = edge_user_indicators
# threshold = 0.95
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['Ótimo', 'Justo', 'Aleatório']
# xsc = 1e6
# -----------------------------------------
#           Graph 3
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'pairing/pairing_mean_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'pairing/pairing_mean_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'pairing/pairing_mean_cell'
# # loc = 'lower right'
# threshold = 0.95
# func = cdf2mean
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['Ótimo', 'Justo', 'Aleatório']
# xsc = 1e6
# -----------------------------------------
#           Graph 4
# -----------------------------------------
# # _type = graph_type['jain_pair']
# # fn = 'pairing/pairing_fair_pair'
# # loc = 'upper right'
# # _type = graph_type['jain_gain']
# # fn = 'pairing/pairing_fair_gain'
# # loc = 'upper right'
# threshold = 0.05
# func = cdf2mean
# ylab = 'Índice de justiça de Jain'
# xlab = 'Número de EU'
# label = ['Ótimo', 'Justo', 'Aleatório']
# xsc = 1
# curves =  get_curves(cases, n_users, n_curves, _type, func, threshold)
# plt.plot_uppa([curves[0], curves[1], curves[2]], save=True, filename=fn, lab=label, ylab=ylab, xlab=xlab, xscale=xsc, lpos=loc)
#==============================================================================
#            Power allocation
#==============================================================================
# -----------------------------------------
#           Graph 1
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'power_allocation/pa_cell_edge_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'power_allocation/pa_cell_edge_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'power_allocation/pa_cell_edge_cell'
# # loc = 'lower right'
# func = edge_user_indicators
# threshold = 0.05
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['Justo', 'Fixo']
# xsc = 1e6
# -----------------------------------------
#           Graph 2
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'power_allocation/pa_nearest_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'power_allocation/pa_nearest_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'power_allocation/pa_nearest_cell'
# # loc = 'upper right'
# func = edge_user_indicators
# threshold = 0.95
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['Justo', 'Fixo']
# xsc = 1e6
# -----------------------------------------
#           Graph 3
# -----------------------------------------
# # user
# # _type = graph_type['user']
# # fn = 'power_allocation/pa_mean_user'
# # loc = 'upper right'
# # pairs
# # _type = graph_type['subband']
# # fn = 'power_allocation/pa_mean_pair'
# # loc = 'upper right'
# # cell
# # _type = graph_type['cell']
# # fn = 'power_allocation/pa_mean_cell'
# # loc = 'lower right'
# threshold = 0.95
# func = cdf2mean
# ylab = 'Taxa de dados [Mbps]'
# xlab = 'Número de EU'
# label = ['Justo', 'Fixo']
# xsc = 1e6
# -----------------------------------------
#           Graph 4
# -----------------------------------------
# # _type = graph_type['jain_pair']
# # fn = 'power_allocation/pa_fair_pair'
# # loc = 'upper right'
# # _type = graph_type['jain_gain']
# # fn = 'power_allocation/pa_fair_gain'
# # loc = 'upper right'
# threshold = 0.05
# func = cdf2mean
# ylab = 'Índice de justiça de Jain'
# xlab = 'Número de EU'
# label = ['Justo', 'Fixo']
# xsc = 1   
# curves =  get_curves(cases, n_users, n_curves, _type, func, threshold)
# plt.plot_uppa([curves[1], curves[3]], save=True, filename=fn, lab=label, ylab=ylab, xlab=xlab, xscale=xsc, lpos=loc)