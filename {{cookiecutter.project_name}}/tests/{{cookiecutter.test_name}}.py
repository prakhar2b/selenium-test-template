import yaml
import pytest

file_name = "../../test.yml"

class Feature(object):
	def __init__(self, d):
		for a, b in d.items():
			if isinstance(b, (list, tuple)):
			   setattr(self, a, [Feature(x) if isinstance(x, dict) else x for x in b])
			else:
			   setattr(self, a, Feature(b) if isinstance(b, dict) else b)



def get_test_feature(file_name):
	with open(file_name, 'r') as test_f:
		try:
			tf = yaml.safe_load(test_f)  # test_feature 
		except yaml.YAMLError as exc:
			print(exc)

	tf = Feature(tf)

	test_name = tf.test.name
	base_url = tf.test.base_url
	global_step_wait = tf.test.step_wait
	steps = tf.test.steps


	return test_name, base_url, global_step_wait, steps


def test_google(driver_):
	test_name, base_url, global_step_wait, steps = get_test_feature(file_name)
	global driver 
	driver = driver_
	driver.get(base_url)
	"""
	Sample selenium test

	1. Conftest setup
	2. Run all steps sequentially
	"""

	driver.get(base_url)
	try:
		driver.implicitly_wait(global_step_wait)
		for step in steps:
			print("x")
			do_steps(step, driver)
		print("done")
	except Exception as ex:
		print(ex)
	driver.quit()
