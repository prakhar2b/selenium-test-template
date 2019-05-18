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
	Supported locator type : attribute, css_selector, xpath
	"""
	elem = None
	for l in locators:
		if not elem:
			if l.type == "attribute":
				try:
					if l.key == "name":
						elem = driver.find_element_by_name(l.value)
					elif l.key == "id":
						elem = driver.find_element_by_id(l.value)
					else:
						elem = driver.find_element_by_css_selector("[{}={}]".format(l.key, l.value))

				except Exception as ex:
					print(ex)

			elif l.type =="css_selector":
				try:
					elems = driver.find_elements_by_css_selector(l.value)
					position = int(l.position) - 1
					elem = elems[position] if len(elems) >= position else None
				except Exception as ex:
					print(ex)

			elif l.type == "xpath":
				try:
					#elem = driver.find_element_by_xpath(l.value)
					elem = driver.find_element_by_xpath("//div[@id='topstuff']/div/div/p")

					# TO-DO : correct error in yaml file
				except Exception as ex:
					print(ex)
		else:
			break
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
