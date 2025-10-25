import logging
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

import ast

from traduction import *

langue="en"

texte_de_début_du_programme="# Ce programme a etais generer par PyCreator\n# https://github.com/smartin187/PyCreator\n# Si vous souhaiter publier ce programme, veuiller mentionner PyCreator\n\n"

def exporter_le_programme(fichier_liste, langue_pour_gestionaire_de_fichier):
    """Cette fonction crée un fichier python grace au fichier dans la liste"""
    logging.debug("entrer dans la fonction d'export")
    global langue
    langue=langue_pour_gestionaire_de_fichier

    fichier_tmp=""
    fichier_tmp=fichier_tmp+texte_de_début_du_programme
    
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
        Path(chemain_d_accé_fichier_export).write_text(fichier_tmp)




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
        Path(chemain_d_accé_fichier).write_text(str(liste_fichier))

def ouvrir_un_fichier_PPyC(langue_pour_gestionaire_de_fichier):
    """Cette fonction ouvre un fichier PPyC. Cela convertit le fichier en liste avec chaque élément en dicionnaire. Return cette liste."""
    global langue
    langue=langue_pour_gestionaire_de_fichier
    
    chemain_d_accé_fichier_ouverture=filedialog.askopenfilename(title=trad_aaach[langue],filetypes=[(trad_aaacf[langue], "*.PPyC")])
    logging.debug("chemain d'ouverture : " + chemain_d_accé_fichier_ouverture)
    if chemain_d_accé_fichier_ouverture!="":
        fichier_ouverture=open(chemain_d_accé_fichier_ouverture, "r", encoding="ANSI")
        fichier_tmp_pour_ouverture=fichier_ouverture.read()

        fichier_convertit_en_liste = ast.literal_eval(fichier_tmp_pour_ouverture)

        logging.debug("Convertion du fichier en liste réussit, liste de dicitonnaire : ")
        logging.debug(fichier_convertit_en_liste)

        return fichier_convertit_en_liste
    else:
        return "Annuler"