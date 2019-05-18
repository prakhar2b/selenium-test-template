#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author : Prakhar Pratyush <prakharlabs@gmail.com>
#
#----------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def until_url_changed(driver, max_wait):
	# https://seleniumhq.github.io/selenium/docs/api/py/
	# webdriver_support/selenium.webdriver.support.expected_conditions.html
	# #selenium.webdriver.support.expected_conditions.url_changes

	"""
	From documentation

	class url_changes(object):
	    def __init__(self, url):
	        self.url = url

	    def __call__(self, driver):
	        return self.url != driver.current_url
	"""
	WebDriverWait(driver, float(max_wait)).until(EC.url_changes(driver))


def get_elem(locators, driver):
	"""
	Supported locator type : (Ref- https://selenium-python.readthedocs.io/locating-elements.html)
		1. Attribute (id, name) => {key, value}
		2. CSS Selectors        => {value}
		3. Xpath                => {value}
		4. Tag
		5. Link text (Complete/ Partial)
		6. Class name

	Note:
		1. You can specify multiple locators which will be checked in successive order if previous ones fail.
		2. If position is specified, expect multiple matching elements

	"""
	elems = None


	for l in locators:
		if elems:
			break
		else:
			#
			try:
				p_flag = bool(l.position) # Position
			except Exception as ex:
				p_flag = 0

			#########################################################################
			####                  By Attribute (name, id)                    ########
			#########################################################################

			if l.type == "attribute":
				try:
					if l.key == "name":
						elems = driver.find_elements_by_name(l.value) if p_flag else \
								driver.find_element_by_name(l.value)

					elif l.key == "id":
						elems = driver.find_elements_by_id(l.value) if p_flag else \
								driver.find_element_by_id(l.value)

					else:
						elems = driver.find_elements_by_css_selector("[{}={}]".format(l.key, l.value)) if p_flag else \
								driver.find_element_by_css_selector("[{}={}]".format(l.key, l.value))


				except Exception as ex:
					print(ex)

			#########################################################################
			####                    By CSS Selector                          ########
			#########################################################################

			elif l.type =="css_selector":
				try:
					elems = driver.find_elements_by_css_selector(l.value) if p_flag else \
							driver.find_element_by_css_selector(l.value)

				except Exception as ex:
					print(ex)

			#########################################################################
			####                    By CSS xpath                             ########
			#########################################################################

			elif l.type == "xpath":
				try:
					elems = driver.find_elements_by_xpath(l.value)  if p_flag else \
							driver.find_element_by_xpath(l.value)

				except Exception as ex:
					print(ex)

	if  p_flag:
		position = int(l.position) - 1
		elem = elems[position] if len(elems) >= position else None

	return elem

def do_steps(step, driver):
	"""
	interface for all the supported selenium test steps
	"""

	if step.type == "input":
		text = step.text
		step_wait = step.config.step_wait
		elem = get_elem(step.locators, driver)

		if not elem:
			raise Exception("Test Failed at step 1")

		elem.send_keys(text)
		driver.implicitly_wait(step_wait)

	elif step.type == "click":
		step_wait = step.config.step_wait
		elem = get_elem(step.locators, driver)
		if not elem:
			raise Exception("Test Failed at Step 2")
		elem_type = elem.get_attribute("type")
		if elem_type == "submit":
			elem.submit()
		else:
			elem.click()
		driver.implicitly_wait(step_wait)

	elif step.type == "assertion":
		step_wait = step.config.step_wait
		elem = get_elem(step.locators, driver)

		assertion_type = step.assertionType

		if assertion_type == "textExists":
			assert elem.text.__contains__(step.value)
			driver.implicitly_wait(step_wait)
		else:
			if assertion_type == "elementNotExists":
				try:
					elem = get_elem(step.locators)
					assert False, "Found element with id idres"
				except Exception:
					assert True
				driver.implicitly_wait(step_wait)
		

	elif step.type == "wait":
		until_url_changed(driver, step.value)
		driver.implicitly_wait(step.config.step_wait)

	else:
		raise Exception("The step type is not supported.")
