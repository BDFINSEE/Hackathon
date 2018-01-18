#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 12:14:27 2018

@author: ZAFAR
"""

#%%
#importons un fichier test
import pandas as pd
#Nettoyage du fichier_rp
fichier_rp=pd.read_csv("rp_2017_01.csv",sep=";")
fichier_rp["NUMVOI_X"] = "%.2g" % row.fichier_rp["NUMVOI_X"]
fichier_rp=fichier_rp.fillna('')
fichier_rp["NUMVOI_X"]=fichier_rp["NUMVOI_X"].replace()

 #%%%%%%
 ##A) Pages jaunes
from lxml import etree
import requests
import pandas as pd
import re

#ex_ville='59122-cambrai'
#ex_nom='tereos'
#ex_ville='ile-de-france'
#ex_nom='gifi'

def nettoyage_espaces(chaine):
    ch=chaine
    while len(ch)>0 and ch[0]==' ':
        ch=ch[1:]
    return ch

test={'nom_ent': 'BROCELIANDE', 'num_voie': '', 'type_voie': '', 'nom_voie': nan, 'code_postal': '', 'dep': '', 'commune': 'VILLERS BOCAGE', 'bis_ter': '', 'adresse_complete': 'nan'}

def recup_PJ(ligne_ent): 
#    ligne_ent=test
    nom=ligne_ent["nom_ent"]
    if ligne_ent["type_voie"]!="":
        ville=ligne_ent["type_voie"]+"-"
    else:
        ville=""
    if ligne_ent["nom_voie"]!="" and str(ligne_ent["nom_voie"])==ligne_ent["nom_voie"]:
        ville=ville+ligne_ent["nom_voie"].replace(" ","-")+"-"
    if ligne_ent["commune"]!="":
        ville=ville+ligne_ent["commune"]+"-"
    if ligne_ent["dep"]!="":
        ville=ville+ligne_ent["dep"]+"-"
    elif ligne_ent["commune"]=="":
        ville=ville+ligne_ent["code_postal"]+"-"
    ville=ville[:-1]
    url='https://www.pagesjaunes.fr/recherche/'+ville+'/'+nom
    r=requests.post(url)
    contenu=r.text
    tree = etree.HTML(contenu)
    result_names= tree.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "denomination-links", " " ))]')
    result_addresses=tree.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "adresse", " " ))]')
    result_secteurs=tree.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "activites", " " ))]')
#    #TEST####
#    len(result_names)==len(result_addresses)
#    len(result_names)==len(result_secteurs)
#    #######
    n=len(result_names)
    tab=[]
    for i in range(n):
        #Le nom
        name=result_names[i].text.split("\n")[1]
        name=nettoyage_espaces(name)
        #L'adresse (en deux étapes)
        addr=result_addresses[i].text.split("\n")[2].split(",")[0]
        addr=nettoyage_espaces(addr)
        town=result_addresses[i].text.split("\n")[2].split(",")[1]
        town=nettoyage_espaces(town)
        postal=''.join([i for i in town if i.isdigit()])
#        #Le secteur d'activité
#        sector=result_secteurs[i].text.split("\n")[1]
#        sector=nettoyage_espaces(sector)
        tab.append([name,postal])
    return pd.DataFrame(tab)

test={'nom_ent': 'GENDARMERIE NATIONALE', 'num_voie': '2', 'type_voie': 'Rue', 'nom_voie': 'DE CHATEAUBRIAND', 'code_postal': '1053', 'dep': '', 'commune': '', 'bis_ter': '', 'adresse_complete': '2 Rue DE CHATEAUBRIAND'}

  
#if name=__main__:

    
    
#%%Pour copier quelque-chose dans le presse-papier

import pyperclip
pyperclip.copy(contenu)


    
    
    
    