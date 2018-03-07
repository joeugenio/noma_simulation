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
import logzero
from logzero import logger
import numpy as np

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

logger.info('Creating grid with 19 sites')
my_grid = net.Grid()

logger.info('Deploing base stations on grid')
my_grid.deploy_base_station()

logger.info('Deploing users equipments on grid')
my_grid.deploy_user_equipment('hexagon')

logger.info('Starting all base stations')
my_grid.start_all_base_stations()

logger.info('Connecting UE to best BS')
my_grid.connect_all_ue()

inter = my_grid.user_equipments[0].received_interference(my_grid.sites)
pwr = my_grid.user_equipments[0].received_power_connected(my_grid.sites)
print(inter, pwr)
print(utl.dbm2watts(pwr)/utl.dbm2watts(inter))

# logger.info('Plotting grid figures')
# plt.plot_grid(my_grid, sh=True, save=False, connect=True)

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