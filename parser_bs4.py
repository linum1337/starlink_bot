from bs4 import BeautifulSoup
import codecs
from parser_selenium import login_form


f = codecs.open('cabinet.html', 'r', 'utf-8')
html = f.read()
soup = BeautifulSoup(html, 'lxml')
def balance_parser(soup):
        a = soup.find('td', {'class': 'tarif-head tarif-current'})
        for i in a:
            if i == '<h4>Основной тариф: 0.0 руб. / мес.</h4>':
                print(i)
print(balance_parser(soup))