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
# log level DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

logger.info('Creating grid with 19 sites')
my_grid = net.Grid()

logger.info('Deploing base stations on grid')
my_grid.deploy_base_station()
logger.info('Deploing users equipments on grid')
my_grid.deploy_user_equipment()
logger.info('Ploting grid figures')


# TESTE
print(my_grid.base_stations[3].status)

my_grid.base_stations[3].startBS()

print(my_grid.base_stations[3].status)

print(my_grid.base_stations[3].id)
print(my_grid.base_stations[3].cells[0].id)
print(my_grid.base_stations[3].cells[0].ant)
print(my_grid.user_equipments[6].id)

#plt.plot_grid(my_grid, sh=True, save=False, sh_hex=False)

