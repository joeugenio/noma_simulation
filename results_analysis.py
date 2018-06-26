#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 08/05/2018
# Last update: 07/05/2018
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
cases_noma = ['cell_sbb/noma2', 'cell_sbb/noma6', 'cell_sbb/noma10', 'cell_sbb/noma20', 'cell_sbb/noma30']
cases_oma = ['cell_sbb/oma2', 'cell_sbb/oma6', 'cell_sbb/oma10', 'cell_sbb/oma20', 'cell_sbb/oma30']
noma = []
oma = []
for i in range(5):
    noma.append(np.load(const.OUT_PATH+cases_noma[i]+'.npy')[0])
    oma.append(np.load(const.OUT_PATH+cases_oma[i]+'.npy')[0])
noma_20 = np.load(const.OUT_PATH+'users_avg/noma_user_20.npy')[0]
oma_20 = np.load(const.OUT_PATH+'users_avg/oma_user_20.npy')[0]
noma_30 = np.load(const.OUT_PATH+'users_avg/noma_user_30.npy')[0]
oma_30 = np.load(const.OUT_PATH+'users_avg/oma_user_30.npy')[0]

logger.info('Plot graphs: Throughout CDF')
# #==============================================================================
# # case 2 users, user throughout 
# logger.info('Plot Users Throughout CDF (2 UE per cell)')
# n = (noma[0].thr[:70:3]/1e6, 1-noma[0].cdf[0][:70:3]/10000)
# o = (oma[0].thr[:70:3]/1e6, 1-oma[0].cdf[0][:70:3]/10000)
# label = ['NOMA 2 EU', 'OMA 2 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_user_2', lab=label)

# # case 6 users, user throughout 
# logger.info('Plot Users Throughout CDF (6 UE per cell)')
# n = (noma[1].thr[:50:2]/1e6, 1-noma[1].cdf[0][:50:2]/10000)
# o = (oma[1].thr[:50:2]/1e6, 1-oma[1].cdf[0][:50:2]/10000)
# label = ['NOMA 6 EU', 'OMA 6 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_user_6', lab=label)

# # case 10 users, user throughout 
# logger.info('Plot Users Throughout CDF (10 UE per cell)')
# n = (noma[2].thr[:15:]/1e6, 1-noma[2].cdf[0][:15:]/10000)
# o = (oma[2].thr[:15:]/1e6, 1-oma[2].cdf[0][:15:]/10000)
# label = ['NOMA 10 EU', 'OMA 10 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_user_10', lab=label)

# # case 20 users, user throughout
# logger.info('Plot Users Throughout CDF (20 UE per cell)')
# n = (noma_20.thr/1e6, 1-noma_20.cdf[0])
# o = (oma_20.thr/1e6, 1-oma_20.cdf[0])
# label = ['NOMA 20 EU', 'OMA 20 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_user_20', lab=label)

# case 30 users, user throughout
# logger.info('Plot Users Throughout CDF (30 UE per cell)')
# n = (noma_30.thr/1e6, 1-noma_30.cdf[0])
# o = (oma_30.thr/1e6, 1-oma_30.cdf[0])
# label = ['NOMA 30 EU', 'OMA 30 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_user_30', lab=label)

# #==============================================================================
# # case 2 users, cell throughout 
# logger.info('Plot Cell Average Throughout CDF (2 UE per cell)')
# n = (noma[0].thr[::3]/1e6, 1-noma[0].cdf[1][::3]/10000)
# o = (oma[0].thr[::3]/1e6, 1-oma[0].cdf[1][::3]/10000)
# label = ['NOMA 2 EU', 'OMA 2 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_cell_2', lab=label)

# # case 6 users, cell throughout 
# logger.info('Plot Cell Average Throughout CDF (6 UE per cell)')
# n = (noma[1].thr[::3]/1e6, 1-noma[1].cdf[1][::3]/10000)
# o = (oma[1].thr[::3]/1e6, 1-oma[1].cdf[1][::3]/10000)
# label = ['NOMA 6 EU', 'OMA 6 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_cell_6', lab=label)

# # case 10 users, cell throughout 
# logger.info('Plot Cell Average Throughout CDF (10 UE per cell)')
# n = (noma[2].thr[::3]/1e6, 1-noma[2].cdf[1][::3]/10000)
# o = (oma[2].thr[::3]/1e6, 1-oma[2].cdf[1][::3]/10000)
# label = ['NOMA 10 EU', 'OMA 10 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_cell_10', lab=label)

# # case 20 users, cell throughout 
# logger.info('Plot Cell Average Throughout CDF (20 UE per cell)')
# n = (noma[3].thr[::3]/1e6, 1-noma[3].cdf[1][::3]/1e4)
# o = (oma[3].thr[::3]/1e6, 1-oma[3].cdf[1][::3]/1e4)
# label = ['NOMA 20 EU', 'OMA 20 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_cell_20', lab=label)

# # case 30 users, cell throughout 
# logger.info('Plot Cell Average Throughout CDF (30 UE per cell)')
# n = (noma[4].thr[::3]/1e6, 1-noma[4].cdf[1][::3]/1e4)
# o = (oma[4].thr[::3]/1e6, 1-oma[4].cdf[1][::3]/1e4)
# label = ['NOMA 30 EU', 'OMA 30 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_cell_30', lab=label)

# # ==============================================================================
# # case 2 users, subband average throughout 
# logger.info('Plot Subband Average Throughout CDF (2 UE per cell)')
# n = (noma[0].thr[::3]/1e6, 1-noma[0].cdf[2][::3]/10000)
# o = (oma[0].thr[::3]/1e6, 1-oma[0].cdf[2][::3]/10000)
# label = ['NOMA 2 EU', 'OMA 2 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_sbb_2', lab=label)

# # case 6 users, subband average throughout 
# logger.info('Plot Subband Average Throughout CDF (6 UE per cell)')
# n = (noma[1].thr[:50:2]/1e6, 1-noma[1].cdf[2][:50:2]/10000)
# o = (oma[1].thr[:50:2]/1e6, 1-oma[1].cdf[2][:50:2]/10000)
# label = ['NOMA 6 EU', 'OMA 6 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_sbb_6', lab=label)

# # case 10 users, subband average throughout 
# logger.info('Plot Subband Average Throughout CDF (10 UE per cell)')
# n = (noma[2].thr[:30:]/1e6, 1-noma[2].cdf[2][:30:]/10000)
# o = (oma[2].thr[:30:]/1e6, 1-oma[2].cdf[2][:30:]/10000)
# label = ['NOMA 10 EU', 'OMA 10 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_sbb_10', lab=label)

# # case 20 users, subband average throughout 
# logger.info('Plot Subband Average Throughout CDF (20 UE per cell)')
# n = (noma_20.thr[::2]/1e6, 1-noma_20.cdf[1][::2])
# o = (oma_20.thr[::2]/1e6, 1-oma_20.cdf[1][::2])
# label = ['NOMA 20 EU', 'OMA 20 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_sbb_20', lab=label)

# # case 30 users, subband average throughout 
# logger.info('Plot Subband Average Throughout CDF (30 UE per cell)')
# n = (noma_30.thr[::2]/1e6, 1-noma_30.cdf[1][::2])
# o = (oma_30.thr[::2]/1e6, 1-oma_30.cdf[1][::2])
# label = ['NOMA 30 EU', 'OMA 30 EU']
# plt.plot_cdf_noma_oma(n, o, save=True, filename='cdf_sbb_30', lab=label)
# # ==============================================================================

# logger.info('Plot graphs: Cell Spectral Efficiency')
# cdf_pn = 95
# cdf_po = 95
# m = 1
# noma_effic = []
# oma_effic = []
# for cdf_pn, cdf_po in [(5,5),(50,50),(95,95)]:
#     noma_max_effic = []
#     for i in range(5):
#         n = noma[i].cdf[m]/1e2
#         for j in range(100):
#             if (n[j]>=cdf_pn):
#                 print(n[j], noma[i].thr[j]/1e6, j)
#                 t = noma[i].thr[j]
#                 noma_max_effic.append(t)
#                 break
#     oma_max_effic = []
#     for i in range(5):
#         o = oma[i].cdf[m]/1e2
#         for j in range(100):
#             if (o[j]>=cdf_po):
#                 print(o[j], oma[i].thr[j]/1e6, j)
#                 t = oma[i].thr[j]
#                 oma_max_effic.append(t)
#                 break
#     noma_effic.append(noma_max_effic)
#     oma_effic.append(oma_max_effic)

# users = np.array([2,6,10,20,30])
# n = np.array(noma_effic)/10e6
# o = np.array(oma_effic)/10e6
# n_label = ['NOMA FCP 5%', 'NOMA FCP 50%', 'NOMA FCP 95%']
# o_label = ['OMA FCP 5%', 'OMA FCP 50%', 'OMA FCP 95%']
# label = [n_label,o_label]
# plt.plot_multi_user_gain(n, o, users, save=True, lab=label, filename='cell_effic')

# # ==============================================================================
logger.info('Load data from files')

coeff_noma = ['power_coefficiet/noma_2ue_coeff_0.0', 'power_coefficiet/noma_2ue_coeff_0.2',
'power_coefficiet/noma_2ue_coeff_0.4','power_coefficiet/noma_2ue_coeff_0.6',
'power_coefficiet/noma_2ue_coeff_0.8','power_coefficiet/noma_2ue_coeff_1.0']

coeff_oma = ['power_coefficiet/oma_2ue_coeff_0.0', 'power_coefficiet/oma_2ue_coeff_0.2',
'power_coefficiet/oma_2ue_coeff_0.4','power_coefficiet/oma_2ue_coeff_0.6',
'power_coefficiet/oma_2ue_coeff_0.8','power_coefficiet/oma_2ue_coeff_1.0']
noma = []
oma = []
n_point = len(coeff_noma)

for i in range(n_point):
    noma.append(np.load(const.OUT_PATH+coeff_noma[i]+'.npy')[0])
    oma.append(np.load(const.OUT_PATH+coeff_oma[i]+'.npy')[0])

logger.info('Plot graphs: Cell Spectral Efficiency')
cdf_pn = 95
cdf_po = 95
m = 0
noma_alloc = []
oma_alloc = []
for cdf_pn, cdf_po in [(50,50),(95,95)]:
    noma_effic = []
    for i in range(n_point):
        n = noma[i].cdf[m]*1e2
        for j in range(100):
            if (n[j]>=cdf_pn):
                # print(n[j], j)
                t = noma[i].thr[j]
                noma_effic.append(t)
                break
    oma_effic = []
    for i in range(n_point):
        o = oma[i].cdf[m]*1e2
        for j in range(100):
            if (o[j]>=cdf_po):
                # print(o[j], j)
                t = oma[i].thr[j]
                oma_effic.append(t)
                break
    noma_alloc.append(noma_effic)
    oma_alloc.append(oma_effic)

coeff = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])
n = np.array(noma_alloc)/10e6
o = np.array(oma_alloc)/10e6
n_label = ['NOMA FCP 50%', 'NOMA FCP 95%']
o_label = ['OMA FCP 50%', 'OMA FCP 95%']
label = [n_label,o_label]
plt.plot_coeff_gain(n, o, coeff, sh=True, lab=label, filename='coeff_gain')
# # ==============================================================================

# logger.info('Plot graphs: Cell-Edge Spectral Efficiency')
# logger.info('Load data from files')

# noma = []
# oma = []
# users_set = [2, 6, 10, 20, 30]
# for i in users_set:
#     noma.append(np.load(const.OUT_PATH+'users_avg/noma_user_'+str(i)+'.npy')[0])
#     oma.append(np.load(const.OUT_PATH+'users_avg/oma_user_'+str(i)+'.npy')[0])

# cdf =  4.5
# noma_user = []
# m = 0
# for case in noma:
#     n = case.cdf[m]*1e2
#     for j in range(len(n)):
#         if (n[j] >= cdf):
#             t = case.thr[j]
#             # print(n[j], t, j)
#             noma_user.append(t)
#             break
# oma_user = []
# for case in oma:
#     n = case.cdf[m]*1e2
#     for j in range(len(n)):
#         if (n[j] >= cdf):
#             t = case.thr[j]
#             # print(n[j], t, j)
#             oma_user.append(t)
#             break

# # normalizes the throughput (spectral efficiency)
# users = np.array(users_set[1::])
# n = np.array(noma_user[1::])/const.BW #*users
# o = np.array(oma_user[1::])/const.BW #*users

# label = ['NOMA ', 'OMA']
# plt.plot_cell_edge_user(n, o,  users, save=True, lab=label, filename='cell_edge')