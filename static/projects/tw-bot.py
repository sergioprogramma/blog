from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


EMAIL = "-"
PASSWORD = "-"
PHONENUMBER = "-"

chrome_driver_path = "/Users/sergioburigana/Desktop/Python/chromedriver"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://twitter.com/i/flow/login")

time.sleep(6)
email_field = driver.find_element(by=By.NAME, value='text')
email_field.send_keys(EMAIL)
email_field.send_keys(Keys.ENTER)
time.sleep(2)

try:
    password = driver.find_element(by=By.NAME, value='password')
    password.send_keys(PASSWORD)
    password.send_keys(Keys.ENTER)
except:
    phonenumber = driver.find_element(by=By.NAME, value='text')
    phonenumber.send_keys(PHONENUMBER)
    phonenumber.send_keys(Keys.ENTER)
    time.sleep(2)
    password = driver.find_element(by=By.NAME, value='password')
    password.send_keys(PASSWORD)
    password.send_keys(Keys.ENTER)

time.sleep(2)
driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div').send_keys("Just testing")
post_bt = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span').click()
