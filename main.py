#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 31/01/2018
# Version: 1.0

# Main Python Script for NOMA communications simulations

import nomalib.channel as ch
import nomalib.scenario as scn
import nomalib.utils as utl
import nomalib.plots as plt
import logzero
from logzero import logger
import numpy as np

# create log files
# log level DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('INFO: NOMA system level simulation starting')

logger.info('INFO: Creating grid with 19 sites')
my_grid = scn.Grid()

logger.info('INFO: Deploing users equipments on grid')
my_grid.deploy_users_equipment()
plt.plot_grid(my_grid, True, '--g')

logger.info('INFO: Creating hexagon object')
my_hex = utl.Hexagon(r=250, center=utl.Coordinate(100,-200))
# plt.plot_hexagon(my_hex)
