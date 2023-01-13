from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
import lxml
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

        time.sleep(4)
        cookies = driver.get_cookies()
        #request_parser(cookies)
        return cookies
        #time.sleep(5)


    except Exception as ex:
        return ex

    finally:
        driver.close()
        driver.quit()
    return 1
def request_parser(cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
    }
    requests_cookies = {}
    for c in cookies:
        requests_cookies[c['name']] = c['value']
    responce = requests.get('https://www.cabinet.levokumka.net/cabinet/welcome/', cookies=requests_cookies,
                            headers=headers)

    #print(responce.text)
    #balance_parse(responce)
    lic_bill = requests.get('https://www.cabinet.levokumka.net/cabinet/%d0%9b%d0%b8%d1%86%d0%b5%d0%b2%d0%be%d0%b9-%d1%81%d1%87%d0%b5%d1%82/', cookies=requests_cookies,headers=headers)
    soup_main = BeautifulSoup(responce.text, 'lxml')
    soup_bill = BeautifulSoup(lic_bill.text,'lxml')
    return soup_main, soup_bill

def tarif_parse(soup):

    a = soup.findAll('h4')
    info = str(a[1])
    return info[4:-5]

def balance_parse(soup):
    p = soup.findAll('td')
    info_p = str(p[3])
    return info_p[4:-5]

#login_form('BILL0000139', '5ormvx')