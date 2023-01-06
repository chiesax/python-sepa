import pandas as pd

from sepa.home.config import TRANS_FILE


def get_category(*cats):
    return '/'.join(cats)


SALUTE = 'Salute'
ALIMENTAZIONE = 'Alimentazione'
TELEFONO = 'Telefono'
TASSE = 'Tasse'
BENZINA = 'Benzina'
ABITI = 'Abiti'
PRELEVAMENTO = 'Prelevamento'
CHARGES_PPE = 'Charges_PPE'
ENERGIA = 'Energia'
INTERNET = 'Internet'
ANIMALI = 'Animali'
AUTOMOBILE = 'Automobile'
CARTA_DI_CREDITO = 'Carta_di_credito'
SPICCIOLI = 'Spiccioli'
TRANSF_IPOTECA = get_category('Trasferimento', 'Ipoteca')
ASSICURAZIONI = 'Assicurazioni'
ATTIVITA = 'Attivita'


simple_matching = {'HELSANA VERSICHERUNGEN AG': SALUTE,
                   'CSS KRANKEN-VERSICHERUNG AG': SALUTE,
                   'CSS Kranken-Vers. AG': SALUTE,
                   'ASSURA': SALUTE,
                   'SWISSCOM': TELEFONO,
                   'DEPARTEMENT DES FINANCES': TASSE,
                   'Etat de Neuchâtel': TASSE,
                   'Migros MMM Marin Cen': ALIMENTAZIONE,
                   'MCDONALDS': ALIMENTAZIONE,
                   'MC DONALD': ALIMENTAZIONE,
                   'Brasserie Wok Royal': ALIMENTAZIONE,
                   'Migros M Portes-Roug': ALIMENTAZIONE,
                   'Migrol Service': BENZINA,
                   'C & A Mode': ABITI,
                   'Denner NE-Sablons': ALIMENTAZIONE,
                   'Denner Satellit': ALIMENTAZIONE,
                   'Retrait BM': PRELEVAMENTO,
                   'PPE Résidence du Verger': CHARGES_PPE,
                   'PPE Résidence le Verger': CHARGES_PPE,
                   'Denner Marin-Epagnier': ALIMENTAZIONE,
                   'Dosenbach Chauss': ABITI,
                   'VITEOS SA': ENERGIA,
                   'Sunrise UPC Sagl': INTERNET,
                   'GLORY DONUTS': ALIMENTAZIONE,
                   'QUALIPET': ANIMALI,
                   'Tamoil': BENZINA,
                   'Manora Rest': ALIMENTAZIONE,
                   'IKIRU RESTAURANT': ALIMENTAZIONE,
                   'GB Véhitechnique SA': AUTOMOBILE,
                   'CAISSE DES MEDECINS': SALUTE,
                   'Prélèvement automate CHF': PRELEVAMENTO,
                   'RED PEPPER': ALIMENTAZIONE,
                   'Viseca Payment Services SA': CARTA_DI_CREDITO,
                   'Chiesa Samuele et LIne': TRANSF_IPOTECA,
                   'Denner Discount ': ALIMENTAZIONE,
                   'Aldi Suisse': ALIMENTAZIONE,
                   'Coop-1217 St-Blais': ALIMENTAZIONE,
                   'Buvette du Port': ALIMENTAZIONE,
                   'Shell': BENZINA,
                   'Pharmacie': SALUTE,
                   'Amavita': SALUTE,
                   'SOCAR': BENZINA,
                   'Migrol Sugiez': BENZINA,
                   'Assura-Basis SA': SALUTE,
                   'Zurich Versicherungsgesellschaft': ASSICURAZIONI,
                   'Zurich Compagnie Assurance': ASSICURAZIONI,
                   'Sun Store': SALUTE,
                   'Football Club Hauterive': ATTIVITA,
                   'CSS Kranken-Versicherung': SALUTE,
                   'Swisscom (Schweiz) AG': TELEFONO,
                   'Viteos SA': ENERGIA,
                   'Sunrise Sagl': INTERNET
                   }

if __name__ == '__main__':
    trans = pd.read_csv(TRANS_FILE, sep='\t')
    categorized = 0
    categories = []
    for index, row in trans.iterrows():
        cat = ''
        if str(row['category']) != 'nan':
            categories.append(row['category'])
            continue
        info = row['additional_information']
        for k, v in simple_matching.items():
            if k in info:
                cat = v
                break
        if row['value'] <= 10:
            cat = SPICCIOLI
        if cat:
            categorized += 1
        categories.append(cat)
    print('Found {}/{} categories'.format(categorized, len(trans)))
    trans['category'] = categories
    trans.to_csv(TRANS_FILE, sep='\t', index=False)

    debits = trans[trans['credit_debit_indicator'].str.contains('DBIT')]['value'].sum()
    uncat = trans[(trans['credit_debit_indicator'].str.contains('DBIT')) & (trans['category'] == '')]['value'].sum()

    pass