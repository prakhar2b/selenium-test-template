#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author : Prakhar Pratyush <prakharlabs@gmail.com>
#
#----------------------------------------------------------

import pytest
from tests.helpers import do_steps

test_config = {{cookiecutter.test_config}}

def test_google(driver_):
	base_url = test_config['base_url']
	global_step_wait = test_config['global_step_wait']
	steps = test_config['steps']
	
	global driver 
	driver = driver_
	driver.get(base_url)

	driver.implicitly_wait(global_step_wait)
	
	for step in steps:
		do_steps(step, driver)
	
	driver.quit()
