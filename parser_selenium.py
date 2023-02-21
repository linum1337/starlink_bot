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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

def login_form(login, pwd): #Проход логина, сохранение куки

    log = str(login)
    pas = str(pwd)
    options = webdriver.ChromeOptions()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')


    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    url = "https://www.cabinet.levokumka.net/cabinet/"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:

        driver.get(url=url)
        driver.set_window_size(1439, 818)
        driver.find_element(By.ID, "pass-field").send_keys(pas)
        driver.find_element(By.ID, "login-field").send_keys(log)
        driver.find_element(By.ID, "pass-field").send_keys(Keys.ENTER)
        driver.find_element(By.CSS_SELECTOR, ".actions:nth-child(3) > .btn").click()

        time.sleep(1)
        cookies = driver.get_cookies()
        #request_parser(cookies)
        return cookies
        #time.sleep(5)


    except:
        return 0

    finally:
        driver.close()
        driver.quit()
def request_parser(cookies):  #Преобразование полученых страниц для дальшнейшего прасинга
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
    services = requests.get('https://www.cabinet.levokumka.net/cabinet/%d1%83%d0%bf%d1%80%d0%b0%d0%b2%d0%bb%d0%b5%d0%bd%d0%b8%d0%b5-%d1%83%d1%81%d0%bb%d1%83%d0%b3%d0%b0%d0%bc%d0%b8/', cookies=requests_cookies, headers=headers)
    lic_bill = requests.get('https://www.cabinet.levokumka.net/cabinet/%d0%9b%d0%b8%d1%86%d0%b5%d0%b2%d0%be%d0%b9-%d1%81%d1%87%d0%b5%d1%82/', cookies=requests_cookies,headers=headers)
    soup_main = BeautifulSoup(responce.text, 'lxml')
    soup_bill = BeautifulSoup(lic_bill.text,'lxml')
    soup_services = BeautifulSoup(services.text, 'lxml')
    return soup_main, soup_bill, soup_services      #Возвращение преобразованных страниц

def tarif_parse(soup): #Получение текущего тарифа

    a = soup.findAll('h4')
    info = str(a[1])
    print(info)
    return info[4:-5]

def client_parse(soup):
    p = soup.findAll('p')
    return p
def balance_parse(soup): #Получение текущего баланса
    p = soup.findAll('td')
    info_p = str(p[3])
    return info_p[4:-5]

def req_payment_parse(soup): #получение обещанного платежа
    td = soup.findAll('i')
    return td


def lic_parse(soup):
    td = soup.findAll('td')
    return td
def req_payment_ryl(soup):
    p_r = soup.findAll('p')
    print(p_r)

def helpdesk_sender(cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
    }
    payload = {

        'subject': 'Тест',
        'message': 'Тест',
        'module_token_unique': 'bc8daa48718fc3d921fdbd4ee7e1a8f4887',
        'module_token': 'bc8daa48718fc3d921fdbd4ee7e1a8f4',

    }
    requests_cookies = {}
    print(cookies)
    for c in cookies:
        requests_cookies[c['name']] = c['value']
    print(requests_cookies)
    #log = str(login)
    #pas = str(pwd)
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    url = "https://www.cabinet.levokumka.net/cabinet/"
    driver = webdriver.Chrome(
        executable_path="/chromedriver",
        options=options,
    )
    try:
        driver.get("https://www.cabinet.levokumka.net/cabinet/welcome/")
        driver.add_cookie(requests_cookies)
        driver.get("https://www.cabinet.levokumka.net/cabinet/welcome/")
        driver.set_window_size(1440, 818)
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, ".col-xs-15:nth-child(1)").click()
        driver.find_element(By.ID, "subject").click()
        driver.find_element(By.ID, "subject").send_keys("dsf")
        driver.find_element(By.ID, "message_helpdesk").click()
        driver.find_element(By.ID, "message_helpdesk").send_keys("sdags")
        driver.find_element(By.CSS_SELECTOR, ".modal-footer > .btn-primary").click()
    except Exception as ex:
        return ex


    finally:
        driver.close()
        driver.quit()

    return True
#login_form('BILL0000139', '5ormvx')