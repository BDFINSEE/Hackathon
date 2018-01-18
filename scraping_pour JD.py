
# coding: utf-8

# In[1]:


get_ipython().magic('pylab inline')


# In[20]:


import pandas as pd
from pprint import pprint


# In[5]:



# In[83]:


import re

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


# In[51]:


data_dept = 'rp_2017_14.csv'


# In[135]:


import re


df = pd.read_csv(data_dept, sep=';', encoding='ISO-8859-1')

df2=df.loc[range(20,40),]

#liste_resultats
for row in df2.itertuples():
    ent = extrait_ent(row)
    print(ent)
    a=recup_PJ(ent)
    print(a)

    
    
    
    # Appel PJ
    # TODO
    # resultats_pj = crawl_pagesjaunes(ent)
    
    # Appel X
    # TODO
    # resultats_x = crawl_x(ent)
    
    
    #pprint(ent)
    


# In[130]:


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
    if row.ILT_X == 1:
        cp = row.DEPCOM_CODE if str(row.DEPCOM_CODE) != 'nan'  else ''
        ent['code_postal']= str(cp).strip()
    else: 
        ent['code_postal']= ''
    
    dep = "%.5g" % row.DLT_X
    dep = dep if str(dep) != 'nan'  else ''
    ent['dep'] = dep
    
    ville = row.CLT_X if str(row.CLT_X) != 'nan'  else ''
    ent['commune'] = ville
    
    bis_ter = row.BISTER_X if str(row.BISTER_X) != 'nan'  else ''
    ent['bis_ter'] = bis_ter
    
    adresse_complete = "%s %s %s %s" % (ent['num_voie'], ent['bis_ter'], 
                                     ent['type_voie'], ent['nom_voie'])
    ent['adresse_complete'] = re.sub('  +', ' ', adresse_complete).strip(' ')
    
    
    # Activite
    
    
    return ent
    


# In[145]:


# https://www.societe.com/cgi-bin/liste?nom=MATRA+ELECTRONIQUE&dirig=&pre=&ape=&dep=60

import requests


def crawl_societe_com(ent):

    url = 'https://www.societe.com/cgi-bin/liste?nom='

    # Construire le nom d'entreprise     
    s = re.sub('  +', ' ', ent['nom_ent']).strip(' ')
    nom_ent = '+'.join(s.split())
    
    # A suivre
    url_complete = '' # TODO
 
    response = requests.get(url_complete)
    
    if response.status_code != 200:
        print('Échec de la requête: statut %s.' % response.status_code)

    resultats = list()
    # TODO Recupere les resultats depuis la requete
    
    return resultats


# In[133]:


import re

def clean_text(string):
    """Fonction de nettoyage textuel sommaire."""
    # Remplace les tabluations, sauts de lignes, etc. par des espaces.
    string = re.sub('\n|\r|\t|\xa0', ' ', string)
    # Retire les ' .' (séparateurs utilisés dans `soup.get_text`) inappropriés.
    string = re.sub('^\.', '', string.replace(' .', ''))
    # Retire les espaces inappropriés.
    return re.sub('  +', ' ', string).strip(' ')


# In[146]:


pwd

