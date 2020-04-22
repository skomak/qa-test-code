'''
Created on 10 kwi 2020

@author: skomak
'''

import pytest

from selenium.webdriver import Chrome

@pytest.fixture(scope='package')
def browser():
    driver = Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
   
    yield driver
    driver.quit()