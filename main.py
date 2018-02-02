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
import logzero
from logzero import logger
import matplotlib.pyplot as plt
import numpy as np

# create log files
# log level DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('INFO: NOMA system level simulation starting')

loss1 = ch.PropagationModel()
loss2 = ch.PropagationModel(env='urban', fc=900)
loss3 = ch.PropagationModel(env='rural', fc=900)
loss3 = ch.PropagationModel(env='rural', fc=2000)

logger.info('INFO: Create grid with 19 sites')
grid = scn.Grid(r=250)
x = y = np.array([])

for i in grid.coord:
    for j in i:
        print(type(j))
        
print(grid)