import itertools

from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    with open('/home/samuele/PycharmProjects/python-sepa/sepa/examples/One_2022_01_08_pag1.html', 'r') as f:
        d = f.read()
    soup = BeautifulSoup(d, 'html.parser')

    #print(soup.get_text())
    st = soup.find_all('div', class_='table-item')
    details = soup.find_all('strong', id=re.compile('^transaction-details'))
    dates = soup.find_all(id=re.compile('transaction-date-item-date'))
    am = soup.find_all(id=re.compile('^transaction-info-amount'))
    curr = soup.find_all(id=re.compile('^transaction-info-currency'))

    for p in itertools.zip_longest(details, dates, am, curr):
        print([p[0].attrs['id'].replace('transaction-details-', '')] + [x.text for x in p])



