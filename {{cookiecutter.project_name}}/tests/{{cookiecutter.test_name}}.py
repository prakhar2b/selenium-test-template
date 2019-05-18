#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author : Prakhar Pratyush <prakharlabs@gmail.com>
#
#----------------------------------------------------------

import pytest
from tests.helpers import do_steps

class Objectify(object):
	def __init__(self, d):
		for a, b in d.items():
			if isinstance(b, (list, tuple)):
			   setattr(self, a, [Objectify(x) if isinstance(x, dict) else x for x in b])
			else:
			   setattr(self, a, Objectify(b) if isinstance(b, dict) else b)
			
test_config = {{cookiecutter.test_config}}
test_config = Objectify(test_config)

def {{cookiecutter.test_name|lower|replace(' ', '_')}}(driver_):
	ase_url = test_config.base_url
	global_step_wait = test_config.global_step_wait
	steps = test_config.steps
	
	global driver 
	driver = driver_
	driver.get(base_url)

	driver.implicitly_wait(global_step_wait)
	
	for step in steps:
		do_steps(step, driver)
	
	driver.quit()
