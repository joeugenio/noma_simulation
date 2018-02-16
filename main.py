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

logger.info('Creating channel')
my_ch = ch.Channel()

logger.info('Deploing base stations on grid')
my_grid.deploy_base_station()

logger.info('Deploing users equipments on grid')
my_grid.deploy_user_equipment()

logger.info('Starting all base stations')
my_grid.start_all_base_stations()

logger.info('Connecting UE to nearest BS')
my_grid.connect_all_to_cell(my_ch)

# logger.info('Plotting grid figures')
# plt.plot_grid(my_grid, sh=True, save=False, connect=False)

# logger.info('Plotting attenuation figures')
# plt.plot_cell_attenuation(my_grid.base_stations[9], 1, my_ch, sh=True)
# plt.plot_bs_attenuation(my_grid.base_stations[9], my_ch, sh=True)

plt.plot_shadow_uncorrelated(sh=True)