#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author : Prakhar Pratyush <prakharlabs@gmail.com>
#
#----------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_condition(condition, max_wait, driver):
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
	if condition == "url_changed":
		WebDriverWait(driver, max_wait).until(EC.url_changes(driver))


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
			####                    By  xpath                                ########
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
	A Step can be a user action of type:
		1. Input (Enter Text)
		2. Click, Double click
		3. Wait        =>   Implicit or Explicit
		4. Assertion
		5. Drag and drop, etc.
	"""

	step_wait = step.config.step_wait

	#########################################################################
	####                        Input                                ########
	#########################################################################

	if step.type == "input":
		"""
		Different type of steps have different possible attributes.
		You are open to play along with the yaml spec and make 
		any changes as you deem fit.

		To support dynamic input fields like -
			1. Text Box (Enter Text)
			2. Radio Button
			3. Check Box/ Drop Down etc.

		We need to have a separate parameter in yaml input file

		step.type = input
		step.subtype = textbox/ radiobutton etc
		"""

		elem = get_elem(step.locators)

		if not elem:
			raise Exception("No element found. Test Failed.")

		if step.subtype == "textbox":
			text = step.text
			elem.send_keys(text)



	#########################################################################
	####                        Click                                ########
	#########################################################################

	elif step.type == "click":
		elem = get_elem(step.locators)

		if not elem:
			raise Exception("No element found. Test Failed.")

		elem_type = elem.get_attribute("type")

		if elem_type == "submit":
			elem.submit()
		else:
			elem.click()


	#########################################################################
	####                        Assertion                            ########
	#########################################################################

	elif step.type == "assertion":

		assertion_type = step.assertionType

		if assertion_type == "textExists":
			elem = get_elem(step.locators)
			if not elem:
				raise Exception("No element found. Test Failed.")
			assert elem.text.__contains__(step.value)
			
		else:

			if assertion_type == "elementNotExists":

				try:
					elem = get_elem(step.locators)
					assert False, "Found element with id idres"

				except Exception:
					assert True
				

	#########################################################################
	####                Wait ( Explicit / Implicit)                  ########
	#########################################################################

	elif step.type == "wait":
		try:
			flag_until = bool(l.until) # Conditions
		except Exception as ex:
			flag_until = 0

		if flag_until:
			wait_condition(step.until, step.value, driver)
		else:
			driver.implicitly_wait(step.value)

		driver.implicitly_wait(step.config.step_wait)

	else:
		raise Exception("The step type is not supported.")

	driver.implicitly_wait(step_wait)
