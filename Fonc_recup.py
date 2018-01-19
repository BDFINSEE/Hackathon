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


def requete_PJ(nom,ville):
    url='https://www.pagesjaunes.fr/recherche/'+ville+'/'+nom
    r=requests.post(url)
    contenu=r.text
    tree = etree.HTML(contenu)
    result_names= tree.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "denomination-links", " " ))]')
    result_addresses=tree.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "adresse", " " ))]')
    return (contenu,result_names,result_addresses)
    
import re 

def decoupe_adresse(adresse):
    #Expression régulière Farid
    p = re.compile(r"\D*([\d*\s]*).([Bb]is|ter)*\s*(r|bd|pl|rte|av|ra|cours|all|crs|zac|\s)\s*(.*),\s*(\d+)\s(.*)$", re.IGNORECASE)
    m = p.match(adresse)
    num_voi=m.group(1)
    bister=m.group(2)
    if bister==None:
        bister=""
    type_voi=m.group(3)
    nom_voi=m.group(4)
#    postal_code=m.group(5)
    vil=m.group(6)
    return [nom_voi,num_voi,type_voi,bister,"",vil]

adresse='81 83 bd République, 24500 EYMET'
adresse='66 La Canebière, 13001    MARSEILLE'

decoupe_adresse(adresse)


def recup_PJ(cabbi,ligne_ent):
    ligne_ent=test
    tab=[]
    j=0
    if str(ligne_ent["nom_ent"])==ligne_ent["nom_ent"]:
        nom=ligne_ent["nom_ent"]
    else:
        j=12
        #return [] -> ça cesse la fonction ?
    while j<2:
        if ligne_ent["nom_voie"]!="" and str(ligne_ent["nom_voie"])==ligne_ent["nom_voie"] and j==0:
            if ligne_ent["type_voie"]!="":
                ville=ligne_ent["type_voie"]+"-"
            else:
                ville=""
            ville=ville+ligne_ent["nom_voie"].replace(" ","-")+"-"
        else:
            ville=""
        if ligne_ent["commune"]!="":
            ville=ville+ligne_ent["commune"]+"-"
        if ligne_ent["dep"]!="":
            ville=ville+ligne_ent["dep"]+"-"
        elif ligne_ent["commune"]=="":
            ville=ville+ligne_ent["code_postal"]+"-"
        ville=ville[:-1]
        (contenu,result_names,result_addresses)=requete_PJ(nom,ville)
        n=len(result_names)
        n=min(n,1)
        if n>0:
            j=10
            for i in range(n):
                #Le nom
                name=result_names[i].text.split("\n")[1]
                name=nettoyage_espaces(name)
                #L'adresse (adresse totale, puis ville découpée en code postal vrai et nom)
                addr_all=result_addresses[i].text.split("\n")[2]
                addr=result_addresses[i].text.split("\n")[2].split(",")[0]
                addr=nettoyage_espaces(addr)
                town=result_addresses[i].text.split("\n")[2].split(",")[1]
                town=nettoyage_espaces(town)
                postal=''.join([i for i in town if i.isdigit()])
                town_pure=''.join([i for i in town if i.isdigit()==False])
                #Résultat
                ligne=[cabbi,name]+decoupe_adresse(addr_all)
                tab.append(ligne)
        else:
            j=j+1
    return tab

test={'nom_ent': 'GENDARMERIE NATIONALE', 'num_voie': '2', 'type_voie': 'Rue', 'nom_voie': 'DE CHATEAUBRIAND', 'code_postal': '1053', 'dep': '', 'commune': '', 'bis_ter': '', 'adresse_complete': '2 Rue DE CHATEAUBRIAND'}

    
    
#%%Pour copier quelque-chose dans le presse-papier

import pyperclip
pyperclip.copy(contenu)


    
    
    
    