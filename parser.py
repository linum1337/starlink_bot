import requests
from bs4 import BeautifulSoup
import fake_useragent
session = requests.Session()
link = 'https://www.cabinet.levokumka.net/cabinet/'
user = fake_useragent.UserAgent().random
header = {
    'user-agent': user,

}

data = {
    'form_sent': '1',
    'LOGIN': 'BILL0000139',
    'PASSWD': '5ormvx',

}

responce = session.post(link, data=data, headers=header)

lk_main = 'https://www.cabinet.levokumka.net/cabinet/welcome/'

lk_responce = session.get(lk_main).text

print(lk_responce)