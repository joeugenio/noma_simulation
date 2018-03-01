#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 31/01/2018
# Version: 1.0

# Main Python Script for NOMA communications simulations

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

# logger.info('Creating channel')
# my_ch = ch.Channel()

logger.info('Deploing base stations on grid')
my_grid.deploy_base_station()

logger.info('Deploing users equipments on grid')
my_grid.deploy_user_equipment('hexagon')

logger.info('Starting all base stations')
my_grid.start_all_base_stations()

logger.info('Connecting UE to best BS')
my_grid.connect_all_ue()

# logger.info('Plotting grid figures')
# plt.plot_grid(my_grid, sh=True, save=False, connect=False)

# logger.info('Plotting attenuation figures')
# plt.plot_cell_attenuation(my_grid.sites[9], 1, sh=True)
# plt.plot_bs_attenuation(my_grid.sites[9], sh=True)

logger.info('Plot shadow fading map')
plt.plot_shadow(my_grid.sites[0].channel, sh=True)


# TESTE
s1 = my_grid.sites[0].channel.shadow.shw_map
s2 = my_grid.sites[1].channel.shadow.shw_map
# print('COV', np.cov(s1)/s1.var())
s1 = s1.reshape(s1.size)
s2 = s2.reshape(s2.size)
print('CORR', np.correlate(s1,s2)/s1.size)
# print('COV', np.cov(s2)/s2.var())
# print('STD', s1.std(), s2.std()/np.sqrt(.5))