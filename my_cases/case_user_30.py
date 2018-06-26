#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 07/05/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Case study with 30 users per cell

import nomalib.simulator as sim
import logzero
from logzero import logger
import __main__ as main

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/'+main.__file__[2:-3:]+'.log', mode='a', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# create simulation
s = sim.Simulator(n_ue_cell=30)
# create scenario
s.scenario_generator()
# run simulator
s.run()