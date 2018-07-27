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
simul_case02 = np.load(const.OUT_PATH+'simul_case2ue.npy')
simul_case04 = np.load(const.OUT_PATH+'simul_case4ue.npy')
simul_case06 = np.load(const.OUT_PATH+'simul_case6ue.npy')
simul_case08 = np.load(const.OUT_PATH+'simul_case8ue.npy')
simul_case10 = np.load(const.OUT_PATH+'simul_case10ue.npy')
simul_case20 = np.load(const.OUT_PATH+'simul_case20ue.npy')
simul_case30 = np.load(const.OUT_PATH+'simul_case30ue.npy')

logger.info('Plot graphs: Throughout CDF')
graph_type = {'user':0, 'cell':1, 'subband':2, 'jain_user':3, 'jain_pair':4, 'jain_gain':5}
gt = 'jain_gain'
i = graph_type[gt]
#==============================================================================
# case 30 users, user throughout 
# i = 0
logger.info('Plot Users Throughout CDF (30 UE per cell)')
c = []
for j in range(4):
    c.append(simul_case30[j*6+i])
label = ['Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, save=True, filename='cdf_30_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================
# case 20 users, user throughout 
# i = 5
logger.info('Plot Users Throughout CDF (20 UE per cell)')
c = []
for j in range(4):
    c.append(simul_case20[j*6+i])
label = ['Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, save=True, filename='cdf_20_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================
# case 10 users, user throughout 
# i = 0
logger.info('Plot Users Throughout CDF (10 UE per cell)')
c = []
for j in range(4):
    c.append(simul_case10[j*6+i])
label = ['Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, save=True, filename='cdf_10_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================
# case 8 users, user throughout 
# i = 5
logger.info('Plot Users Throughout CDF (8 UE per cell)')
c = []
for j in range(4):
    c.append(simul_case08[j*6+i])
label = ['Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, save=True, filename='cdf_8_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================
# case 6 users, user throughout 
# i = 0
logger.info('Plot Users Throughout CDF (6 UE per cell)')
c = []
for j in range(5):
    c.append(simul_case06[j*6+i])
label = ['Exhaustive', 'Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, save=True, filename='cdf_6_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])

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
plt.plot_cdf(c, save=True, filename='cdf_4_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])

#==============================================================================
# case 2 users, user throughout 
# i = 0
logger.info('Plot Users Throughout CDF (02 UE per cell)')
c = []
for j in range(5):
    c.append(simul_case02[j*6+i])
label = ['Exhaustive', 'Fair', 'Random', 'PA fix', 'OMA']
xlabel = ['Taxa de dados [Mbps]',"Jain's fairness index"]
norma = [1e6, 1]
plt.plot_cdf(c, save=True, filename='cdf_2_'+gt, lab=label, xlab=xlabel[i//3], norma=norma[i//3])
