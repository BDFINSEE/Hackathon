# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 06:24:44 2018

@author: RANVIER Martial
"""

def code_type_voie(type_voie_long):
    ''' Remplace un type de voie long par son code API Siren court'''
    CORRES = ['ALL Allée',
              'AV Avenue',
              'BD Boulevard',
              'CAR Carrefour',
              'CHE Chemin',
              'CHS Chaussée',
              'CITE Cité',
              'COR Corniche',
              'CRS Cours',
              'DOM Domaine',
              'DSC Descente',
              'ECA Ecart',
              'ESP Esplanade',
              'FG Faubourg',
              'GR Grande Rue',
              'GR Grand Rue',
              'HAM Hameau',
              'HLE Halle',
              'IMP Impasse',
              'LD Lieu dit',
              'LOT Lotissement',
              'MAR Marché',
              'MTE Montée',
              'PAS Passage',
              'PL Place',
              'PLN Plaine',
              'PLT Plateau',
              'PRO Promenade',
              'PRV Parvis',
              'QUA Quartier',
              'QUAI Quai',
              'RES Résidence',
              'RLE Ruelle',
              'ROC Rocade',
              'RPT Rond Point',
              'RTE Route',
              'RUE Rue',
              'SEN Sente',
              'SEN Sentier',
              'SQ Square',
              'TPL Terre-plein',
              'TRA Traverse',
              'VLA Villa',
              'VLGE Village']
    
    conv_type_voie = dict()
    for elt in CORRES:
        code, *mots = elt.split(' ')
        libelle     = ' '.join(mots).upper()
        conv_type_voie[libelle] = code
    
    type_voie_court = conv_type_voie.get(type_voie_long, type_voie_long)
    return type_voie_court

code_type_voie('RUE')          
code_type_voie('R')
code_type_voie('AVENUE')                    