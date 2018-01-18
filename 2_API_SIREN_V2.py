# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 15:34:51 2018

@author: HACKATHON
"""

# 0. Packages 
import requests 
import pandas as pd
import os
import re


# 1. Fonctions MR 
def parametrer_requete(nom_ent, 
                       cpl_adr, 
                       num_voie, 
                       bis_ter, 
                       type_voie,
                       nom_voie,
                       commune):
    parametre = 'Denomination:'                          + nom_ent   + \
                ' AND ComplementAdresseEtablissement:'   + cpl_adr   + \
                ' AND NumeroVoieEtablissement:'          + num_voie  + \
                ' AND IndiceRepetitionEtablissement:'    + bis_ter   + \
                ' AND TypeVoieEtablissement:'            + type_voie + \
                ' AND LibelleVoieEtablissement:'         + nom_voie  + \
                ' AND LibelleCommuneEtablissement:'      + commune
    print(parametre)
    return parametre

def requeter_siren_api(url, parametre):
    requete_params = {'q':parametre}
    requete        = requests.get(url, params=requete_params)
    print(requete.text)
    return           requete.json()

def extraire_sirets(data):
    output = dict()
    for record in data['Etablissements']:
        siret   = record['Siren'] + record['Nic']
        ape     = record['UniteLegale']['ActivitePrincipale']
        rs      = record['UniteLegale']['Denomination']
        adresse = ' ' .join([record['Adresse']['NumeroVoieEtablissement'],
                             record['Adresse']['TypeVoieEtablissement'],
                             record['Adresse']['LibelleVoieEtablissement'],
                             record['Adresse']['CodePostalEtablissement'],
                             record['Adresse']['LibelleCommuneEtablissement']])
        output[siret] = {'RS':rs, 'APE':ape, 'ADRESSE': adresse}
    return output
    
def apparier_siret(url, **params):
    parametre = parametrer_requete(**params)
    data      = requeter_siren_api(url, parametre)
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
    ent['nom_ent'] = row.RS_X
    
    # adresse entreprise
    num_voie = "%.5g" % row.NUMVOI_X
    ent['num_voie'] = num_voie if num_voie != 'nan'  else '' 
    
    type_voie = row.TYPEVOI_X if str(row.TYPEVOI_X) != 'nan'  else ''
    ent['type_voie']= map_nom_voie(type_voie)
    
    ent['nom_voie'] = row.NOMVOI_X if row.NOMVOI_X != 'nan'  else ''

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

for record in df.itertuples():
    params = extrait_ent(record)
    apparier_siret(url, **params)
    break
