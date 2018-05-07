#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 07/05/2018
# Last update: 07/05/2018
# Version: 0.1

# Main Python Script for NOMA communications simulations
# Case study with 2 users per cell

import nomalib.simulator as sim
import logzero
from logzero import logger

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/run_case2.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# create simulation
s = sim.Simulator(n_ue_cell=2)
# create scenario
s.scenario_generator()
# run simulator
s.run()