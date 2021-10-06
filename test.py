import urllib.request
from bs4 import BeautifulSoup

import zipfile
import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC

from ContactService import ContactService
from FileContacts import FileContacts

# html = urllib.request.urlopen('http://observatorio.digemid.minsa.gob.pe')
# soup = BeautifulSoup(html, 'html.parser')
# # tags = soup('h2')
# tags = soup('a')
#
# print(f"LINKS PRINCIPALES - ({len(tags)})")
#
# for tag in tags:
#     print(f"{tag.contents[0]} - {tag.get('href')}")
# for article in articles:
#     print(f"${article}")

# trabajando con selenium
# option = webdriver.ChromeOptions()
# option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
driver = webdriver.Firefox()
driver.get('https://www.paginasamarillas.com.pe/servicios/empresa?page=1')
# driver.get('https://www.facebook.com', )

# --------------Para POPUP-----------------
# try:
#     print("Iniciando el popup")
#     WebDriverWait(driver, 3).until(EC.alert_is_present(), 'Timed out waiting for PA creation confirmation popup to appear.')
#     alert = driver.switch_to.alert
#     # alert.send_keys("Hola mundo")
#     alert.accept()
#     print("alert accepted")
# except TimeoutException as err:
#     print(err)
# --------------END Para POPUP-----------------

# driver.find_element_by_xpath("//input[@type='email']").send_keys('yersyn_2604@hotmail.com')
# driver.find_element_by_xpath("//input[@type='password']").send_keys('874521MA')

#
# element_search = driver.find_element_by_id("phone-list-0")
# element_search.send_keys("paracetamol")



