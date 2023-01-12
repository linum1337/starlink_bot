from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from bs4 import BeautifulSoup
def login_form(login, pwd):
    log = str(login)
    pas = str(pwd)
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    url = "https://www.cabinet.levokumka.net/cabinet/"
    driver = webdriver.Chrome(
        executable_path="/Users/vladislavcehov/PycharmProjects/starlink_bot/chromedriver",
        options=options,
    )

    try:

        driver.get(url=url)
        driver.set_window_size(1439, 818)
        driver.find_element(By.ID, "pass-field").send_keys(pas)
        driver.find_element(By.ID, "login-field").send_keys(log)
        driver.find_element(By.ID, "pass-field").send_keys(Keys.ENTER)

        time.sleep(6)
        full_page = driver.page_source
        with open('cabinet.html', 'w') as lk:
            lk.write(full_page)
        time.sleep(5)


    except Exception as ex:
        return ex

    finally:
        driver.close()
        driver.quit()
    return 1