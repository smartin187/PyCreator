import logging
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

import ast

def exporter_le_programme(fichier_liste):
    """Cette fonction crée un fichier python grace au fichier dans la liste"""
    logging.debug("entrer dans la fonction d'export")
    fichier_tmp=""
    for element in fichier_liste:
        fichier_tmp=fichier_tmp+element["Python"]+"\n"
    
    logging.debug(fichier_tmp)

    chemain_d_accé_fichier_export=filedialog.asksaveasfilename(
        defaultextension=".",
        filetypes=[("Python code source", "*.py")],
        title="Exporter en Python"
    )
    if chemain_d_accé_fichier_export!="":
        Path(chemain_d_accé_fichier_export).write_text(fichier_tmp)




def enregistrer_le_fichier(liste_fichier):
    """Enregistre le fichier en .PPyC"""
    chemain_d_accé_fichier=filedialog.asksaveasfilename(
        defaultextension=".",
        filetypes=[("PyCreator file (Projet Py Creator)", "*.PPyC")],
        title="Enregister le fihcier"
    )
    if chemain_d_accé_fichier!="":
        Path(chemain_d_accé_fichier).write_text(str(liste_fichier))

def ouvrir_un_fichier_PPyC():
    """Cette fonction ouvre un fichier PPyC. Cela convertit le fichier en liste avec chaque élément en dicionnaire. Return cette liste."""
    chemain_d_accé_fichier_ouverture=filedialog.askopenfilename(title="Ouvrir un fichier",filetypes=[("Fichier PyCreator", "*.PPyC")])
    logging.debug("chemain d'ouverture : " + chemain_d_accé_fichier_ouverture)
    if chemain_d_accé_fichier_ouverture!="":
        fichier_ouverture=open(chemain_d_accé_fichier_ouverture, "r", encoding="ANSI")
        fichier_tmp_pour_ouverture=fichier_ouverture.read()

        fichier_convertit_en_liste = ast.literal_eval(fichier_tmp_pour_ouverture)

        logging.debug("Convertion du fichier en liste réussit, liste de dicitonnaire : ")
        logging.debug(fichier_convertit_en_liste)

        return fichier_convertit_en_liste
