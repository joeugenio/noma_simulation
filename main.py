#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 31/01/2018
# Version: 1.0

# Main Python Script for NOMA communications simulations

import nomalib.constants as const
import nomalib.channel as ch
import nomalib.network as net
import nomalib.utils as utl
# import nomalib.plots as plt
import nomalib.simulator as sim
import nomalib.performance as perf
import logzero
from logzero import logger
import numpy as np
from pytictoc import TicToc

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# create simulation
# s = sim.Simulator(mode='cell')
# create scenario
# s.scenario_generator()
# run simulator
# s.run()

# sinr[snaps][sites][cells][ues][ttis]
p = perf.Performance()
N_SINR = 100
sinr = np.load(const.OUT_PATH+'sinr0.npy')
cdf = np.zeros([2,N_SINR])
cdf_thr = np.zeros([2,N_SINR])
cdf_thr2 = np.zeros([2,N_SINR])
sinr_ax = np.linspace(-40,50,N_SINR)
thr_ax = np.linspace(0,15,N_SINR)
thr_ax2 = np.linspace(0,15,N_SINR)

for i in range(len(sinr)):
    for j in range(len(sinr[i])):
        for k in range(len(sinr[i][j])):
            s_ue = [0, 0]
            t_ue = [0, 0]            
            for l in range(len(sinr[i][j][k])):
                s = 0
                t = 0
                for m in range(len(sinr[i][j][k][l])):
                    s += sinr[i][j][k][l][m]
                    t += p.shannon(10*np.log10(sinr[i][j][k][l][m]), bw=1)
                s_ue[l] = s/len(sinr[i][j][k][l])
                t_ue[l] = t/len(sinr[i][j][k][l])
    for n in range(N_SINR):
        for l in range(len(sinr[i][j][k])):
            if (10*np.log10(s_ue[l]) <= sinr_ax[n]):
                cdf[l][n] += 1
            sdb = np.array([10*np.log10(s_ue[l])])
            if (p.shannon(sdb,bw=1) <= thr_ax[n]):
                cdf_thr[l][n] += 1
            if (t_ue[l] <= thr_ax[n]):
                cdf_thr2[l][n] += 1
cdf = cdf/len(sinr)
cdf_thr = cdf_thr/len(sinr)
cdf_thr2 = cdf_thr2/len(sinr)

import matplotlib.pyplot as plt
plt.plot(sinr_ax, cdf[0], '--b', lw=1, label='UE 1')
plt.plot(sinr_ax, cdf[1], '--r', lw=1, label='UE 1')
plt.xlabel('SINR (dB)',fontsize=16)
# plt.ylabel('Throughput (bits/s/Hz)',fontsize=16)
plt.ylabel('CDF',fontsize=16)
plt.grid(True)
plt.title('User SINR Performance', fontsize=16)
plt.legend(fontsize=14, loc=2)

plt.figure(2)
plt.plot(thr_ax, cdf_thr[0], '--b', lw=1, label='UE 1 mean')
plt.plot(thr_ax, cdf_thr[1], '--r', lw=1, label='UE 1 mean')
plt.plot(thr_ax2, cdf_thr2[0], '--g', lw=1, label='UE 1')
plt.plot(thr_ax2, cdf_thr2[1], '--y', lw=1, label='UE 1')
plt.xlabel('Throughput (bits/s/Hz)',fontsize=16)
plt.ylabel('CDF',fontsize=16)
plt.grid(True)
plt.title('User Throughput Performance', fontsize=16)
plt.legend(fontsize=14, loc=2)



plt.show()
# logger.info('Plotting Link Level Performance Model')
# p = perf.Performance()
# plt.plot_l2s(p, sh=True)

# logger.info('Plotting grid scenario')
# plt.plot_grid(s.grid, sh=True, save=False, connect=True)

# c = ch.TemporalChannel()
# logger.info('Plotting  Doppler Filter PSD')
# plt.plot_doppler_filter(c.h[0][0], sh=True)

# logger.info('Plotting  Rayleigh Channel Gain')
# plt.plot_channel_gain(c.h[0][0], sh=True)

# logger.info('Plotting attenuation figures')
# plt.plot_cell_attenuation(my_grid.sites[9], 1, sh=True)
# plt.plot_bs_attenuation(my_grid.sites[9], sh=True)

# logger.info('Plot shadow fading map')
# plt.plot_shadow(input='s9.npy', sh=True)
# # plt.plot_shadow_zoom(input='s9.npy', sh=True)
# ==========================================================================