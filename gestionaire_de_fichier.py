# -*- coding: utf-8 -*-

"""
Module qui gère l'enregistrement, l'ouverture et l'export des fichier.
Cela ouvre les fênetre pour hcoisire l'enplacement des fichier à enregistrer/ouvrir/exporter.
C'est aussi ce module qui crée le code Python générer et qui l'écrit dans un fichier *.py
"""

import logging
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

import ast

from traduction import *

langue="en"


def exporter_le_programme(fichier_liste, langue_pour_gestionaire_de_fichier):
    """Cette fonction crée un fichier python grace au fichier dans la liste"""
    logging.debug("entrer dans la fonction d'export")
    global langue
    langue=langue_pour_gestionaire_de_fichier

    fichier_tmp=""
    fichier_tmp = fichier_tmp + trad_aaagb[langue]      # trad_aaagb contient des commentaire en début du code pour le début du programme
    
    liste_des_action=fichier_liste[1:len(fichier_liste)]
    
    fichier_tmp=fichier_tmp+"\"\"\""+fichier_liste[0]["documentation"]+"\"\"\"\n\n\n"

    for element_de_variable in fichier_liste[0]["variables"]:
        fichier_tmp=fichier_tmp + element_de_variable["Nom"] + "=" + element_de_variable["Valeur par défaut"] + "\n"

    fichier_tmp=fichier_tmp+"\n\n"

    for element in liste_des_action:
        fichier_tmp=fichier_tmp+element["Python"]+"\n"
    
    logging.debug(fichier_tmp)

    chemain_d_accé_fichier_export=filedialog.asksaveasfilename(
        defaultextension=".",
        filetypes=[(trad_aaacd[langue], "*.py")],
        title=trad_aaace[langue]
    )
    if chemain_d_accé_fichier_export!="":
        Path(chemain_d_accé_fichier_export).write_text(fichier_tmp, encoding='utf-8')




def enregistrer_le_fichier(liste_fichier, langue_pour_gestionaire_de_fichier):
    """Enregistre le fichier en .PPyC"""
    global langue
    langue=langue_pour_gestionaire_de_fichier

    chemain_d_accé_fichier=filedialog.asksaveasfilename(
        defaultextension=".",
        filetypes=[(trad_aaacf[langue], "*.PPyC")],
        title=trad_aaacg[langue]
    )
    if chemain_d_accé_fichier!="":
        Path(chemain_d_accé_fichier).write_text(str(liste_fichier), encoding='utf-8')

def ouvrir_un_fichier_PPyC(langue_pour_gestionaire_de_fichier):
    """Cette fonction ouvre un fichier PPyC. Cela convertit le fichier en liste avec chaque élément en dicionnaire. Return cette liste."""
    global langue
    langue=langue_pour_gestionaire_de_fichier
    
    chemain_d_accé_fichier_ouverture=filedialog.askopenfilename(title=trad_aaach[langue],filetypes=[(trad_aaacf[langue], "*.PPyC")])
    logging.debug("chemain d'ouverture : " + chemain_d_accé_fichier_ouverture)
    if chemain_d_accé_fichier_ouverture!="":
        fichier_ouverture=open(chemain_d_accé_fichier_ouverture, "r", encoding="utf-8")
        fichier_tmp_pour_ouverture=fichier_ouverture.read()

        fichier_convertit_en_liste = ast.literal_eval(fichier_tmp_pour_ouverture)

        logging.debug("Convertion du fichier en liste réussit, liste de dicitonnaire : ")
        logging.debug(fichier_convertit_en_liste)

        return fichier_convertit_en_liste
    else:
        return "Annuler"
    

def importer_un_fichier_en_PPyC(langue_pour_gestionaire_de_fichier, fichier_actuelle):
    """Cette fonction permet de sélécionner un fichier (en *.PPyC), et fusionne les deux projet.
    return le nouveau fichier (la fusion)
    """
    global langue
    langue=langue_pour_gestionaire_de_fichier

    chemain_d_accé_fichier_importer_en_PPyC = filedialog.askopenfilename(
        title=trad_aaaig[langue],
        filetypes=[(trad_aaacf[langue], "*.PPyC")]
        )
    
    if chemain_d_accé_fichier_importer_en_PPyC=="":     # l'utilisateur a cliquer sur annuler
        return "Annuller"

    fichier_importation_en_PPyC=open(chemain_d_accé_fichier_importer_en_PPyC, "r", encoding="utf8")

    fichier_tmp_importation=fichier_importation_en_PPyC.read()

    fichier_importation_convertit_en_liste=ast.literal_eval(fichier_tmp_importation)

    # fusion des variables
    for élément_variable in fichier_importation_convertit_en_liste[0]["variables"]:
        fichier_actuelle[0]["variables"].append(élément_variable)
    
    del fichier_importation_convertit_en_liste[0]

    # fusion du code

    for élément in fichier_importation_convertit_en_liste:
        fichier_actuelle.append(élément)
    
    return fichier_actuelle

def importer_un_code_source_python_dans_le_projet(langue_pour_gestionaire_de_fichier, fichier_actuelle):
    """Cette fonction ouvre un projet Python et le fusionne avec le projet PPyC actuelle.
    pour importer le projet python, cela crée des élément personnalisé pour chaque ligne du code python.
    """
    global langue
    langue=langue_pour_gestionaire_de_fichier

    chemain_d_accé_fichier_importer_en_py = filedialog.askopenfilename(
        title=trad_aaaih[langue],
        filetypes=[(trad_aaaii[langue], "*.py")]
        )
    
    if chemain_d_accé_fichier_importer_en_py=="":     # l'utilisateur a cliquer sur annuler
        return "Annuller"

    fichier_importation_en_PPyC=open(chemain_d_accé_fichier_importer_en_py, "r", encoding="utf8")

    fichier_tmp_importation=fichier_importation_en_PPyC.readlines()

    for élément in fichier_tmp_importation:
        fichier_actuelle.append({'humain': trad_aaahb, 'Python': élément, 'type': 'action'})
    
    return fichier_actuelle


