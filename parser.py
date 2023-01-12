import requests
import fake_useragent
url = 'https://www.cabinet.levokumka.net/cabinet'
user = fake_useragent.Us().
def login(un, pwd):
     s = requests.Session()
     payload = {
         'LOGIN': un,
         'PASSWD': pwd,
     }
     res = s.post(url, data=payload, allow_redirects=True)
     lk_profile = 'https://www.cabinet.levokumka.net/cabinet/welcome/'
     lk = s.get(lk_profile)
     return lk

print(login('BILL0000139', '5ormvx').text)