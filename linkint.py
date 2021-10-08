from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from random import randint
import time
import argparse

# parser for options
parser = argparse.ArgumentParser(
    description='linkint can be used to scrape the names of the employes of the target orgnisation.')
parser.add_argument('-e', '--email', type=str, required=True, metavar='',
                    help='email of your account')
parser.add_argument('-p', '--passwd', type=str, required=True, metavar='',
                    help='password of your account')
parser.add_argument('-o', '--org', type=str, required=True, metavar='',
                    help='target orgnisation')
args = parser.parse_args()

# scraping
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.headless = True
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
URL = "https://www.linkedin.com/login"
driver.get(URL)

# options
email = args.email
passwd = args.passwd
org = args.org

try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username.send_keys(email)

    time.sleep(randint(2, 7))

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys(passwd)
    time.sleep(randint(2, 7))
    password.send_keys(Keys.RETURN)

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="global-nav-typeahead"]/input'))
    )
    search.send_keys(org)
    time.sleep(randint(2, 7))
    search.send_keys(Keys.RETURN)

    people = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//li[@class='search-reusables__primary-filter']/button[1]"))
    )
    time.sleep(randint(1, 3))
    people.click()

    for i in range(1, 11):
        names = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='main']/div/div/div[3]/ul/li[{}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]".format(i)))
        )
        print(names.text)

    time.sleep(randint(9, 12))

finally:
    driver.quit()
