import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import time, math, pickle
import pandas as pd

url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=past_12&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first"

driver = webdriver.Chrome()
driver.get(url)

temp = driver.find_element(By.XPATH, '//*[@id="dlMaker_simple"]/dd/ul[1]')
# print(len(temp))

for t in temp:
    print(t.text)


