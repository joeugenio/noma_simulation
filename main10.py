#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Federal University of Campina Grande (UFCG)
# Author: Joel Eugênio Cordeiro Junior
# Date: 28/08/2017
# Last update: 07/05/2018
# Version: 1.0

# Main Python Script for NOMA communications simulations

import nomalib.simulator as sim
import logzero
from logzero import logger

# create log files
# log level: DEBUG=10, INFO=20, WARN=30, ERROR=40
logzero.loglevel(logzero.logging.INFO)
logzero.logfile('./temp/run.log', mode='w', loglevel=logzero.logging.DEBUG)
logger.info('NOMA system level simulation starting')

# create simulation
s = sim.Simulator(n_ue_cell=10)
# create scenario
s.scenario_generator()
# run simulator
s.run()