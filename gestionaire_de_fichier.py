import logging
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)

def exporter_le_programme(fichier_liste):
    """Cette fonction crée un fichier python grace au fichier dans la liste"""
    logging.debug("entrer dans la fonction d'export")
    fichier_tmp=""
    for element in fichier_liste:
        fichier_tmp=fichier_tmp+element["Python"]+"\n"
    logging.debug(fichier_tmp)
    Path("export.py").write_text(fichier_tmp)