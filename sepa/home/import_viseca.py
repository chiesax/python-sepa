import json
import os
import re
import shutil
from datetime import timedelta

import itertools

from bs4 import BeautifulSoup

from sepa.home.config import IMPORT_HISTORY, TRANS_FILE, TRANS_FOLDER, IMPORT_VISECA_FOLDER

import re
import pandas as pd
import dateutil.parser


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
              'details': p[1].text,
              'date': p[2].text,
              'amount': p[3].text,
              'curr': p[4].text} for p in itertools.zip_longest(details, dates, am, curr)]

    trans = [t for t in trans if t['transid'].startswith('TRX')]



