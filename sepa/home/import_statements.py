import json
import os
import re
import shutil
from datetime import timedelta

from sepa.home.config import IMPORT_HISTORY, IMPORT_CAMT53_FOLDER, TRANS_FILE, TRANS_FOLDER

from sepa import parser
import re
import pandas as pd
import dateutil.parser

import_camt53 = os.path.join(IMPORT_CAMT53_FOLDER, 'CAMT053_040123.xml')

if __name__ == '__main__':
    history = None
    if os.path.exists(IMPORT_HISTORY):
        with open(IMPORT_HISTORY, 'r') as f:
            history = json.load(f)
    first_import = None
    last_import = None
    trans = None
    if history:
        first_import = dateutil.parser.isoparse(history['from_to_dates'][0]['from'])
        last_import = dateutil.parser.isoparse(history['from_to_dates'][-1]['to'])
        trans = pd.read_csv(TRANS_FILE)
        shutil.copyfile(TRANS_FILE,
                        os.path.join(TRANS_FOLDER, 'trans_{}_{}.csv'.format(first_import.strftime('%y-%m-%d'),
                                                                            last_import.strftime('%y-%m-%d'))))


    def strip_namespace(xml):
        return re.sub(' xmlns="[^"]+"', '', xml, count=1)


    with open(import_camt53, 'r') as f:
        data_xml = f.read()

    camt_dict = parser.parse_string(parser.bank_to_customer_statement, bytes(strip_namespace(data_xml), 'utf8'))

    if not len(camt_dict['statements']) == 1:
        raise Exception('Expecting exactly a camt53 file with exactly one statement')

    statement = camt_dict['statements'][0]
    statement_from = dateutil.parser.isoparse(statement['from_to_date']['from'])
    statement_to = dateutil.parser.isoparse(statement['from_to_date']['to'])
    if last_import:
        if not (statement_from - timedelta(days=1)).replace(minute=0, second=0, microsecond=0) == last_import.replace(minute=0, second=0, microsecond=0):
            raise Exception('Trying to import a non-consecutive camt53 file')
    statement_entries = []
    if 'entries' in statement:
        for entry in statement['entries']:
            for ed in entry['entry_details']:
                if 'batch' in ed and 'number_of_transactions' in ed['batch'] and int(ed['batch']['number_of_transactions']) > 1:
                    for transaction in ed['transactions']:
                        statement_entries.append({'ref': transaction['refs']['account_servicer_reference'],
                                            'value': transaction['amount']['_value'],
                                            'currency': transaction['amount']['currency'],
                                            'credit_debit_indicator': transaction['credit_debit_indicator'],
                                            'additional_information': ' '.join(*entry['additional_information']),
                                            'related_parties': transaction['related_parties'],
                                            'value_date': entry['value_date']['date'],
                                            'booking_date': entry['booking_date']['date']})
                else:
                    statement_entries.append({'ref': None,
                                        'value': entry['amount']['_value'],
                                        'currency': entry['amount']['currency'],
                                        'credit_debit_indicator': entry['credit_debit_indicator'],
                                        'additional_information': ' '.join(*entry['additional_information']),
                                        'related_parties': None,
                                        'value_date': entry['value_date']['date'],
                                        'booking_date': entry['booking_date']['date']})

    s = sum([float(x['value']) for x in statement_entries])
    if not abs(s - float(statement['transactions_summary']['total_entries']['sum'])) < 0.05:
        raise RuntimeError('Sum of transactions does not match transaction summary.')

    new_trans = pd.DataFrame.from_records(statement_entries)
    if trans:
        trans = pd.concat([trans, new_trans])
    if not history:
        history['from_to_dates'] = []
    history['from_to_dates'].append(statement['from_to_date'])

    with open(IMPORT_HISTORY, 'w') as f:
        json.dump(history, f)
    trans.to_csv(TRANS_FILE)
