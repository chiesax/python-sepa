

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

    with open('/home/samuele/PycharmProjects/python-sepa/sepa/examples/CAMT053_040123_full.xml', 'r') as f:
        data_xml = f.read()

    camt_dict = parser.parse_string(parser.bank_to_customer_statement, bytes(strip_namespace(data_xml), 'utf8'))

    all_entries = []
    for statement in camt_dict['statements']:
        if 'entries' in statement:
            for entry in statement['entries']:
                for ed in entry['entry_details']:
                    if 'batch' in ed and 'number_of_transactions' in ed['batch'] and int(ed['batch']['number_of_transactions']) > 1:
                        for transaction in ed['transactions']:
                            all_entries.append((transaction['refs']['account_servicer_reference'],
                                  transaction['amount']['_value'], transaction['amount']['currency'], transaction['credit_debit_indicator'],
                                  entry['additional_information'], transaction['related_parties'], entry['value_date']['date'], entry['booking_date']['date']))
                    else:
                        all_entries.append((None,
                                  entry['amount']['_value'], entry['amount']['currency'], entry['credit_debit_indicator'],
                                  entry['additional_information'], None, entry['value_date']['date'], entry['booking_date']['date']))

    s = sum([float(x[1]) for x in all_entries])
    pass