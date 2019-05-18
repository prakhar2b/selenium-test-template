from selenium import webdriver
import pytest

@pytest.fixture
def driver_():
	driver = webdriver.Chrome(executable_path = '/home/prakhar/Videos/chromedriver')
	return driver
