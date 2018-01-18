# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 15:34:51 2018

@author: HACKATHON
"""

# 0. Packages 
import requests 
import pandas as pd
import os


# 1. Fonctions MR 
def parametrer_requete(dict_param):
    corr_cle = { 'nom_ent': 'Denomination',
                 'cpl_adr': 'ComplementAdresseEtablissement',
                 'num_voie': 'NumeroVoieEtablissement',
                 'type_voie':'TypeVoieEtablissement',
                 'nom_voie':'LibelleVoieEtablissement',
                 'commune':'LibelleCommuneEtablissement',
                 'bis_ter':'IndiceRepetitionEtablissement'}
    parametre = ''
    for cle, valeur in dict_param.items():
        if len(valeur):
            valeur = valeur.replace(' ', '-')
            parametre  = parametre + corr_cle[cle] + ":" + valeur + " AND "
    parametre = parametre[:-5]
    return parametre

#d_param = {'Denomination':"RANVIER",
#           'NumeroVoieEtablissement':"11"}
#parametrer_requete(d_param)

def requeter_siren_api(url, parametre):
    requete_params = {'q':parametre}
    requete        = requests.get(url, params=requete_params)
#    print(requete.text)
    return           requete.json()

def extraire_sirets(data):
    output = dict()
    if data['Header']['Statut'] == 200:
        for record in data['Etablissements']:
            siret   = record['Siren'] + record['Nic']
            ape     = record['UniteLegale']['ActivitePrincipale']
            rs      = record['UniteLegale']['Denomination']
#            if 'Adresse' in record:
#                try:
#                    adresse = ' ' .join([record['Adresse'].get('NumeroVoieEtablissement',''),
#                                         record['Adresse'].get('TypeVoieEtablissement', ''),
#                                         record['Adresse'].get('LibelleVoieEtablissement',''),
#                                         record['Adresse'].get('CodePostalEtablissement',''),
#                                         record['Adresse'].get('LibelleCommuneEtablissement', '')])
#                    output[siret] = {'RS':rs, 'APE':ape, 'ADRESSE': adresse}
#                except:
#                    print(record['Adresse'])
            output[siret] = {'RS':rs, 'APE':ape}
    return output
    
def apparier_siret(url, d_params):
    parametre = parametrer_requete(d_params)
    data      = requeter_siren_api(url, parametre)
    if data:
        sirets    = extraire_sirets(data)
        return sirets

# 2. Fonctions FO
def map_nom_voie(text):
    """Remplace les noms des voies abreges dans rp par les noms longs"""
    
    streetmap = [
            ('R', 'Rue'), ('AV', 'Avenue'), ('RTE', 'Route'),
            ('CHE', 'Chemin'), ('PL', 'Place'), ('BD', 'Boulevard'),
            ('ALL', 'Allée'), ('IMP', 'Impasse'), ('RN', 'Rond Point'),
            ('CD', 'Chemin Départemental'), ('DOM','Domaine') 
        ] 
    for character in streetmap: 
        if character[0] == text:
            #text = re.sub('[%s]' % character[0], character[1], text)
            text = character[1]
            break
    return text

def extrait_ent(row):    
    ent = dict()
    
    # nom entreprise
    ent['nom_ent'] = row.RS_X if str(row.RS_X) != 'nan'  else ''
    
    # adresse entreprise
    num_voie = "%.5g" % row.NUMVOI_X
    ent['num_voie'] = num_voie if num_voie != 'nan'  else '' 
    
    type_voie = row.TYPEVOI_X if str(row.TYPEVOI_X) != 'nan'  else ''
    ent['type_voie']= map_nom_voie(type_voie)
    
    ent['nom_voie'] = row.NOMVOI_X if str(row.NOMVOI_X) != 'nan'  else ''

    # Si le cp est pas renseigne et que le champs ILT_X=1 alors idem cp personnel
#    if row.ILT_X == 1:
#        cp = row.DEPCOM_CODE if str(row.DEPCOM_CODE) != 'nan'  else ''
#        ent['code_postal']= str(cp).strip()
#    else: 
#        ent['code_postal']= ''
    
#    dep = "%.5g" % row.DLT_X
#    dep = dep if str(dep) != 'nan'  else ''
#    ent['dep'] = dep
    
    ville = row.CLT_X if str(row.CLT_X) != 'nan'  else ''
    ent['commune'] = ville
    
    bis_ter = row.BISTER_X if str(row.BISTER_X) != 'nan'  else ''
    ent['bis_ter'] = bis_ter
    
#    adresse_complete = "%s %s %s %s" % (ent['num_voie'], ent['bis_ter'], 
#                                     ent['type_voie'], ent['nom_voie'])
#    ent['adresse_complete'] = re.sub('  +', ' ', adresse_complete).strip(' ')
    
    # CPLT ADR (MR)
    cpl_adr = row.CPLADR_X if str(row.CPLADR_X) != 'nan'  else ''
    ent['cpl_adr'] = cpl_adr
    
    return ent

# 3. Appel

url = "https://prototype.api-sirene.insee.fr/ws/siret/"    

os.chdir('E:/Hackathon/3_Données/Dept')
df = pd.read_csv(filepath_or_buffer = 'rp_2017_01.csv', 
                 sep =';', 
                 header = 0, 
                 usecols = ['RS_X', 'NOMVOI_X', 'NUMVOI_X', 'TYPEVOI_X',
                            'BISTER_X', 'CPLADR_X', 'CLT_X'])

results = dict()
count_error = 0
for record in df.itertuples():
    params    = extrait_ent(record)
    #print(params)
    parametre = parametrer_requete(params)
    data      = requeter_siren_api(url, parametre)
    if data['Header']['Statut'] != 200:
        print(data['Header']['Statut'])
        count_error += 1
    sirets = apparier_siret(url, params)
    if sirets:
        results.update(sirets)

