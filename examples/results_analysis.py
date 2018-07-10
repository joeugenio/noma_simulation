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
simul_case02 = np.load(const.OUT_PATH+'simul_main.npy')
simul_case04 = np.load(const.OUT_PATH+'simul_main4.npy')
simul_case06 = np.load(const.OUT_PATH+'simul_main6.npy')
# simul_case08 = np.load(const.OUT_PATH+'simul_case_8_users.npy')
# simul_case10 = np.load(const.OUT_PATH+'simul_case_10_users.npy')
# simul_case20 = np.load(const.OUT_PATH+'simul_case_20_users.npy')
# simul_case30 = np.load(const.OUT_PATH+'simul_case_30_users.npy')

logger.info('Plot graphs: Throughout CDF')
graph_type = {'user':0, 'cell':1, 'subband':2, 'r1':3, 'r2':4}
i = graph_type['r1']
# #==============================================================================
# # case 30 users, user throughout 
# i = 0
# logger.info('Plot Users Throughout CDF (30 UE per cell)')
# c = []
# for j in range(4):
#     c.append(simul_case30[j*6+i])
# label = ['Fair', 'Random', 'PA fix', 'OMA']
# plt.plot_cdf(c, sh=True, filename='cdf_30_user', lab=label)

# #==============================================================================
# # case 20 users, user throughout 
# i = 5
# logger.info('Plot Users Throughout CDF (20 UE per cell)')
# c = []
# for j in range(4):
#     c.append(simul_case20[j*6+i])
# label = ['Fair', 'Random', 'PA fix', 'OMA']
# plt.plot_cdf(c, sh=True, filename='cdf_20_user', lab=label)

# #==============================================================================
# # case 10 users, user throughout 
# i = 0
# logger.info('Plot Users Throughout CDF (10 UE per cell)')
# c = []
# for j in range(4):
#     c.append(simul_case10[j*6+i])
# label = ['Fair', 'Random', 'PA fix', 'OMA']
# plt.plot_cdf(c, sh=True, filename='cdf_10_user', lab=label)

# #==============================================================================
# # case 8 users, user throughout 
# i = 5
# logger.info('Plot Users Throughout CDF (8 UE per cell)')
# c = []
# for j in range(5):
#     c.append(simul_case08[j*6+i])
# label = ['Exhaustive', 'Fair', 'Random', 'PA fix', 'OMA']
# plt.plot_cdf(c, sh=True, filename='cdf_8_user', lab=label)

#==============================================================================
# case 6 users, user throughout 
i = 5
logger.info('Plot Users Throughout CDF (6 UE per cell)')
c = []
for j in range(5):
    c.append(simul_case06[j*6+i])
label = ['Exhaustive', 'Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, sh=True, filename='cdf_6_user', lab=label, xlab=xlabel[i//3], norma=norma[i//3])


#==============================================================================
# case 4 users, user throughout 
# i = 0
logger.info('Plot Users Throughout CDF (04 UE per cell)')
c = []
for j in range(5):
    c.append(simul_case04[j*6+i])
label = ['Exhaustive', 'Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, sh=True, filename='cdf_4_user', lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================
# case 2 users, user throughout 
# i = 0
c = []
for j in range(5):
    c.append(simul_case02[j*6+i])
label = ['Exhaustive', 'Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, sh=True, filename='cdf_2_user', lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================

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
# logger.info('Load data from files')

# coeff_noma = ['power_coefficiet/noma_2ue_coeff_0.0', 'power_coefficiet/noma_2ue_coeff_0.2',
# 'power_coefficiet/noma_2ue_coeff_0.4','power_coefficiet/noma_2ue_coeff_0.6',
# 'power_coefficiet/noma_2ue_coeff_0.8','power_coefficiet/noma_2ue_coeff_1.0']

# coeff_oma = ['power_coefficiet/oma_2ue_coeff_0.0', 'power_coefficiet/oma_2ue_coeff_0.2',
# 'power_coefficiet/oma_2ue_coeff_0.4','power_coefficiet/oma_2ue_coeff_0.6',
# 'power_coefficiet/oma_2ue_coeff_0.8','power_coefficiet/oma_2ue_coeff_1.0']
# noma = []
# oma = []
# n_point = len(coeff_noma)

# for i in range(n_point):
#     noma.append(np.load(const.OUT_PATH+coeff_noma[i]+'.npy')[0])
#     oma.append(np.load(const.OUT_PATH+coeff_oma[i]+'.npy')[0])

# logger.info('Plot graphs: Cell Spectral Efficiency')
# cdf_pn = 95
# cdf_po = 95
# m = 0
# noma_alloc = []
# oma_alloc = []
# for cdf_pn, cdf_po in [(50,50),(95,95)]:
#     noma_effic = []
#     for i in range(n_point):
#         n = noma[i].cdf[m]*1e2
#         for j in range(100):
#             if (n[j]>=cdf_pn):
#                 # print(n[j], j)
#                 t = noma[i].thr[j]
#                 noma_effic.append(t)
#                 break
#     oma_effic = []
#     for i in range(n_point):
#         o = oma[i].cdf[m]*1e2
#         for j in range(100):
#             if (o[j]>=cdf_po):
#                 # print(o[j], j)
#                 t = oma[i].thr[j]
#                 oma_effic.append(t)
#                 break
#     noma_alloc.append(noma_effic)
#     oma_alloc.append(oma_effic)

# coeff = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])
# n = np.array(noma_alloc)/10e6
# o = np.array(oma_alloc)/10e6
# n_label = ['NOMA FCP 50%', 'NOMA FCP 95%']
# o_label = ['OMA FCP 50%', 'OMA FCP 95%']
# label = [n_label,o_label]
# plt.plot_coeff_gain(n, o, coeff, sh=True, lab=label, filename='coeff_gain')
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