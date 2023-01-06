
import pandas as pd

from sepa.home.config import TRANS_FILE

if __name__ == '__main__':
    trans = pd.read_csv(TRANS_FILE, sep='\t')
    for index, row in trans.iterrows():

