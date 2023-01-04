

if __name__ == '__main__':
    from sepa import parser
    import re
    import pandas as pd

    data_xml = ('<MndtInitnReq>'
                '<Mndt>'
                '<Authntcn>'
                '<Dt>2017-03-05</Dt>'
                '<Chanl>'
                '<Cd>ABC</Cd>'
                '</Chanl>'
                '</Authntcn>'
                '<MndtId>78904536</MndtId>'
                '<MndtReqId>9823701</MndtReqId>'
                '</Mndt>'
                '<GrpHdr>'
                '<CreDtTm>2017-03-05T13:45:00</CreDtTm>'
                '<Authstn>'
                '<Cd>ILEV</Cd>'
                '</Authstn>'
                '<MsgId>1234567890</MsgId>'
                '</GrpHdr>'
                '</MndtInitnReq>')


    def strip_namespace(xml):
        return re.sub(' xmlns="[^"]+"', '', xml, count=1)

    with open('/home/samuele/PycharmProjects/python-sepa/sepa/examples/CAMT053_040123.xml', 'r') as f:
        data_xml = f.read()

    camt_dict = parser.parse_string(parser.bank_to_customer_statement, bytes(strip_namespace(data_xml), 'utf8'))

    statements = pd.DataFrame.from_dict(camt_dict['statements'])
    all_entries = []
    for i,_ in statements.iterrows():
        if 'entries' in camt_dict['statements'][i]:
            df = pd.DataFrame()
            dd = pd.DataFrame.from_records(camt_dict['statements'][i]['entries'])
            df['Date'] = dd['value_date'].str['date']
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            iban = camt_dict['statements'][i]['account']['id']['iban']
            df['IBAN'] = iban
            df['Currency'] = dd['amount'].str['currency']
            all_entries.append(df)

    df_entries = pd.concat(all_entries)
    pass