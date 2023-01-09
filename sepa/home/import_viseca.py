import os

import itertools

from bs4 import BeautifulSoup

from sepa.home.config import IMPORT_HISTORY, TRANS_FILE, TRANS_FOLDER, IMPORT_VISECA_FOLDER, ONE_FILE

import re
import pandas as pd


import_viseca = os.path.join(IMPORT_VISECA_FOLDER, 'One_2022_01_09_pag1.html')

if __name__ == '__main__':
    with open(import_viseca, 'r') as f:
        data_html = f.read()

    soup = BeautifulSoup(data_html, 'html.parser')

    st = soup.find_all('div', class_='table-item')
    details = soup.find_all('strong', id=re.compile('^transaction-details'))
    dates = soup.find_all(id=re.compile('transaction-date-item-date'))
    am = soup.find_all(id=re.compile('^transaction-info-amount'))
    curr = soup.find_all(id=re.compile('^transaction-info-currency'))

    trans = [{'transid': p[0].attrs['id'].replace('transaction-details-', ''),
              'details': p[0].text,
              'date': p[1].text,
              'amount': p[2].text,
              'category': None,
              'curr': p[3].text} for p in itertools.zip_longest(details, dates, am, curr)]

    trans = [t for t in trans if t['transid'].startswith('TRX')]

    old_trans = None
    if os.path.exists(ONE_FILE):
        old_trans = pd.read_csv(ONE_FILE, sep='\t')
    transids = []
    if old_trans is not None:
        transids = old_trans['transid'].to_list()

    new_trans = [t for t in trans if t['transid'] not in transids]

    trans_df = pd.DataFrame(new_trans)
    if old_trans is not None:
        trans_df = pd.concat([old_trans, trans_df])

    trans_df.to_csv(ONE_FILE, sep='\t', index=False)




