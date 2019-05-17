rom selenium import webdriver
import pytest

@pytest.fixture
def driver():
	global driver
	driver = webdriver.Chrome(executable_path = 'chromedriver')
	return driver
