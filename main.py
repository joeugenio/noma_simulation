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
import nomalib.plots as plt
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
s = sim.Simulator(mode='cell')
# create scenario
s.scenario_generator()
# run simulator
s.run()

# logger.info('Plotting Link Level Performance Model')
# p = perf.Performance()
# plt.plot_l2s(p, sh=True)


# logger.info('Plotting grid scenario')
# plt.plot_grid(s.grid, sh=True, save=False, connect=True)

# t = TicToc()
# t.tic()
# c = ch.TemporalChannel()

# t.toc()
# logger.info('Plotting  Doppler Filter PSD')
# plt.plot_doppler_filter(c.h[0][0], sh=True)

# logger.info('Plotting  Rayleigh Channel Gain')
# plt.plot_channel_gain(c.h[0][0], sh=True)

# logger.info('Plotting attenuation figures')
# plt.plot_cell_attenuation(my_grid.sites[9], 1, sh=True)
# plt.plot_bs_attenuation(my_grid.sites[9], sh=True)

# ==========================================================================
# s0 = np.load(const.DAT_PATH+'s0.npy')
# s1 = np.load(const.DAT_PATH+'s1.npy')
# s2 = np.load(const.DAT_PATH+'s2.npy')

# print(s2.mean(), s2.std(), s2.var())

# s0 = s0.reshape(s0.size)
# s1 = s1.reshape(s1.size)
# s2 = s2.reshape(s2.size)

# print('CORRELATION:',np.correlate(s1,s2)/(s1.size*s1.std()*s2.std()))
# print('CORRELATION:',np.correlate(s0,s1)/(s1.size*s1.std()*s0.std()))

# Run just one time for generate arrays files
# ch.ShadowFadingGenerator().shw_ref_generator(save=False)
# ch.ShadowFadingGenerator().correlation_map_generator()
# for i in range(1,20):
    # ch.ShadowFadingGenerator().inter_site_corr(file='s'+str(i)+'.npy', save=False)
# for i in range(1,20):
    # ch.ShadowFadingGenerator().cross_correlation(file='s'+str(i)+'.npy', save=False)

# logger.info('Plot shadow fading map')
# for i in range(1,20):
    # plt.plot_shadow(input='s'+str(i)+'.npy', sh=True)
    # plt.plot_shadow_zoom(input='s'+str(i)+'.npy', sh=True)