import os

IMPORT_CAMT53_FOLDER = '/home/samuele/money/camt53_import'

TRANS_FOLDER = '/home/samuele/money/trans'
TRANS_FILE = os.path.join(TRANS_FOLDER, 'trans.csv')
IMPORT_HISTORY = os.path.join(TRANS_FOLDER, '.history.json')

if not os.path.exists(IMPORT_CAMT53_FOLDER):
    os.makedirs(IMPORT_CAMT53_FOLDER)

if not os.path.exists(TRANS_FOLDER):
    os.makedirs(TRANS_FOLDER)

