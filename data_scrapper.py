from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

chrome_options = Options()
chrome_options.add_argument("-ignore-certificate-errors")


BASE_URL = "http://www.cresesb.cepel.br/index.php?section=sundata"
s = Service(r"C:/Users/Pdr/Documents/GitHub/UPX003/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)

driver.get(BASE_URL)
sleep(5)