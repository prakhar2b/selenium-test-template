#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author : Prakhar Pratyush <prakharlabs@gmail.com>
#
#----------------------------------------------------------


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def do_condition(condition, max_wait, driver):
	if condition == "url_changed":
		WebDriverWait(driver, max_wait).until(EC.url_changes(driver))