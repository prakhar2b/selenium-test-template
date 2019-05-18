rom selenium import webdriver
import pytest

@pytest.fixture
def driver_():
	driver = webdriver.Chrome(executable_path = 'chromedriver')
	return driver
