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


logger.info('INFO: Creating grid with 19 sites')
grid = scn.Grid()
c = grid.coord
x = np.zeros(len(c))
y = np.zeros(len(c))
for i in range(len(c)):
    x[i] = c[i].x
    y[i] = c[i].y
    # print('X:{} Y:{}'.format(x[i], y[i]))

logger.info('INFO: Deploing users equipments on grid')
grid.deploy_users_equipment()

u = grid.users
x_u = np.zeros(len(u))
y_u = np.zeros(len(u))
for i in range(len(u)):
    x_u[i] = u[i].coord.x
    y_u[i] = u[i].coord.y

# plt.plot(x,y,'^k', ms=10)
# plt.plot(x_u,y_u,'+r')

hex = utl.Hexagon(r=250)
x_h = np.linspace(1,250)
y_h = []
for i in x_h:
    y_h += [hex.f(i)]

plt.plot(x_h,y_h)

plt.show()