"""
Module qui gère l'éditeur de PyCreator.
"""
from tkinter import *
import logging

from gestionaire_de_fichier import *
from traduction import *

logging.basicConfig(level=logging.DEBUG)

fênetre_éditeur_PyCreator=None
espace_de_code=None
code_frame=None

fichier=[]
langue="fr"

def éditeur_PyCreator():
    """Fonction principale de PyCreator"""
    def export():
        """Cette fonction appellèle l'autre fonciton d'export pour avoir l'argument."""
        exporter_le_programme(fichier_liste=fichier)
    
    def enregister_le_fichier_fênetre():
        """Cette fonciton appèle l'autre fonction d'export pour avoir l'argument."""
        enregistrer_le_fichier(liste_fichier=fichier)
    
    def ouvrir_le_fihcier_fênetre():
        """Cette fonction appèlle l'autre fonction d'ouverture pour avoir le retour"""
        global fichier
        fichier=ouvrir_un_fichier_PPyC()
        mise_a_jours_interface_graphique()
    
    global fênetre_éditeur_PyCreator
    global espace_de_code
    global code_frame

    fênetre_éditeur_PyCreator=Tk()
    fênetre_éditeur_PyCreator.title(trad_aaaaa[langue])

    barre_menu_liste_déroulant = Menu(fênetre_éditeur_PyCreator)
    fênetre_éditeur_PyCreator.config(menu=barre_menu_liste_déroulant)

    menu_fichier = Menu(barre_menu_liste_déroulant, tearoff=0)
    barre_menu_liste_déroulant.add_cascade(label=trad_aaaab[langue], menu=menu_fichier)

    menu_fichier.add_command(label=trad_aaaac[langue], command=ouvrir_le_fihcier_fênetre)

    menu_fichier.add_command(label=trad_aaaad[langue], command=enregister_le_fichier_fênetre)

    menu_fichier.add_command(label=trad_aaaae[langue], command=export)

    # espace de code -----------------------------------
    espace_de_code=LabelFrame(fênetre_éditeur_PyCreator, text=trad_aaaaf[langue])
    code_frame=LabelFrame(espace_de_code, text=trad_aaaag[langue])
    ajouter_une_ligne_bouton=Button(code_frame, text=trad_aaaah[langue], command=ajouter_une_ligne).pack()

    espace_de_code.pack()
  
    code_frame.pack()

    

    fênetre_éditeur_PyCreator.mainloop()

fênetre_ajouter_une_ligne=None

valeur_tmp=None
fênetre_ajouter_une_ligne_ecrire_dans_le_terminale=None
fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique=None
def ajouter_une_valeur():
    """Cette fonction est appelé pour ajouter une valeur"""
    
    def chaine_str():
        """Cette fonction permet la définition d'une chaine de caractère."""
        def valider_str():
            """Cette fonction est appelé quand l'utilisateur clique sur validé"""
            global valeur_tmp
            valeur_tmp=chan_texte.get()
            logging.debug(valeur_tmp)
            fênetre_str.destroy()
        fênetre_valeur.destroy()
        
        global chan_texte
        fênetre_str=Toplevel(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique)
        fênetre_str.title(trad_aaaai[langue])
        fênetre_str.grab_set()
        
        texte_fênetre_str=Label(fênetre_str, text=trad_aaaaj[langue]).pack()
        chan_texte=Entry(fênetre_str, width=100)
        chan_texte.pack()
        bouton_valider=Button(fênetre_str, text=trad_jaaaa[langue], command=valider_str).pack()
        fênetre_str.wait_window()

    global fênetre_ajouter_une_ligne_ecrire_dans_le_terminale

    fênetre_valeur=Toplevel(fênetre_ajouter_une_ligne_ecrire_dans_le_terminale)
    fênetre_valeur.title(trad_aaaba[langue])
    fênetre_valeur.grab_set()
    texte_fênetre_valeur=Label(fênetre_valeur, text=trad_aaabb[langue]).pack()
    frame_valeurs_littérales=LabelFrame(fênetre_valeur, text=trad_aaabc[langue])
    bouton_str=Button(frame_valeurs_littérales, text=trad_aaabd[langue], command=chaine_str).pack()
    frame_valeurs_littérales.pack()
    fênetre_valeur.wait_window()

valeur_texte=None
def ajouter_une_ligne():
    """Cette fonction gère l'ajout d'une ligne de code"""
    def bouton_print():
        """Cette fonction est apelé quand l'utilisateur clique sur le bouton print."""
        def définire_la_valeur():
            """Cette fonction définit la valeur du print"""
            ajouter_une_valeur()
            #global valeur_texte
            valeur_pour_print=valeur_tmp
            logging.debug("Valeur pour print : " + valeur_pour_print)
            valeur_du_texte.set(trad_aaabe[langue] + str(valeur_pour_print))
        def valider():
            """Cette fonction valide le print"""
            ligne_de_code_tmp=f"print('{valeur_tmp}')"
            fichier.append({"français":f"Ecrire dans le terminale {valeur_tmp}", "Python":ligne_de_code_tmp})
            logging.debug("fichier : " + str(fichier))
            fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.destroy()
            mise_a_jours_interface_graphique()

        
        global valeur_texte
        global fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique
        valeur_pour_print=None
        global fênetre_ajouter_une_ligne
        fênetre_ajouter_une_ligne.destroy()

        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique=Toplevel(fênetre_éditeur_PyCreator)
        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.grab_set()
        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.title(trad_aaabf[langue])
        texte_fênetre_print=Label(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_aaabg[langue]).pack()
        frame_valeur=LabelFrame(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_aaabh[langue])
        définire_la_valeur=Button(frame_valeur, text=trad_jaaab[langue], command=définire_la_valeur).pack()
        valeur_du_texte = StringVar()
        valeur_du_texte.set(trad_aaabi[langue])
        valeur_texte=Label(frame_valeur, textvariable=valeur_du_texte)
        valeur_texte.pack()
        frame_valeur.pack()
        valider=Button(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_jaaaa[langue], command=valider).pack()
    
    global fênetre_ajouter_une_ligne
    
    fênetre_ajouter_une_ligne = Toplevel(fênetre_éditeur_PyCreator)
    fênetre_ajouter_une_ligne.grab_set()
    fênetre_ajouter_une_ligne.title(trad_jaaac[langue])
    frame_commande_pyhton=LabelFrame(fênetre_ajouter_une_ligne, text=trad_aaabj[langue])
    # bouton pour les fonction python :
    bouton_ajouter_comande_print=Button(frame_commande_pyhton, text=trad_aaaca[langue], command=bouton_print).pack()

    frame_commande_pyhton.pack()
    
    

def mise_a_jours_interface_graphique():
    """Cette fonction permet de metre a jours l'interface graphique, donc d'ajouter / supprimer des lignes de code."""
    def ajouter_ligne_de_code_interface(élément_utiliser:int):
        """Cette fonction ajoute a l'interface graphique un ligne de code."""
        nouvelle_ligne_de_code=LabelFrame(code_frame, text=trad_jaaad[langue])
        texte_humain=Label(nouvelle_ligne_de_code, text=élément_utiliser["français"]).pack()
        texte_python=Label(nouvelle_ligne_de_code, text=élément_utiliser["Python"]).pack()
        nouvelle_ligne_de_code.pack()

    global code_frame
    
    code_frame.destroy()
    code_frame=LabelFrame(espace_de_code, text=trad_aaacb[langue])

    for element in fichier:
        ajouter_ligne_de_code_interface(element)
        
    ajouter_une_ligne_bouton=Button(code_frame, text=trad_aaacc[langue], command=ajouter_une_ligne).pack()
    code_frame.pack()