# -*- coding: utf-8 -*-
"""
Module qui gère l'éditeur de PyCreator.
"""
from tkinter import *
import logging

from gestionaire_de_fichier import *
from traduction import *
import ast
import re

logging.basicConfig(level=logging.DEBUG)

fênetre_éditeur_PyCreator=None
espace_de_code=None
code_frame=None
liste_des_variable_graphique=None
fichier=None
canvas_code=None
scrollbar_code=None


documentation_entrée_texte=None

temps_de_mise_a_jour_interface_graphique=100        # mise a jour de l'interface graphique (apelle de sertaine fonction), pour par exemple la liste box des variables. Cette valeur est en miliseconde.

def apliquer_les_paramètre():
    """Cette fonction applique les paramètre avec le fichier de paramètre"""
    try:
        paramètre_fichier_tmp=open("paramètre.txt", "r", encoding="ANSI")
        
        paramètre_tmp=paramètre_fichier_tmp.read()

        paramètre_tmp=ast.literal_eval(paramètre_tmp)

        logging.debug(paramètre_tmp)

        global langue
        if paramètre_tmp["langue"]=="Français":
            langue="fr"
        elif paramètre_tmp["langue"]=="English":
            langue="en"
    except:
        logging.error("Imposible de charcher les paramètre depuis le fichier 'réglage.txt'")
        langue="en"
        Path("paramètre.txt").write_text(str({"langue":langue}))

def modifier_les_paramètre(fênetre:str):
    """Cette fonction gère la fênetre pour les paramètre"""
    def avertissement_du_changement_de_paramètre():
        """Cette fonction crée une fênetre d'avertissement sur les changement de paramètre, par exemple, si la langue est changé, les paramètre ne serons pas appliquer directement."""
        avertissement_du_changement_de_paramètre_fênetre=Toplevel(fênetre_paramétre)
        avertissement_du_changement_de_paramètre_fênetre.title(trad_aaada[langue])

        texte_avertisement_paramètre=Label(avertissement_du_changement_de_paramètre_fênetre, text=trad_aaadb[langue]).pack()

        bouton_pour_avertisement_paramètre=Button(avertissement_du_changement_de_paramètre_fênetre, text=trad_jaaaa[langue], command=avertissement_du_changement_de_paramètre_fênetre.destroy).pack()

        avertissement_du_changement_de_paramètre_fênetre.grab_set()
        avertissement_du_changement_de_paramètre_fênetre.wait_window()


    def valider():
        """Cette fonction gère la validation des paramètre"""
        langue_tmp=liste_découlante_langue.get()

        Path("paramètre.txt").write_text(str({"langue":langue_tmp}))
        apliquer_les_paramètre()
        
        avertissement_du_changement_de_paramètre()
        logging.debug("Fin de l'avertisement")
        fênetre_paramétre.destroy()


        

    if fênetre=="éditeur":
        fênetre_paramétre=Toplevel(fênetre_éditeur_PyCreator)
    
    fênetre_paramétre.title(trad_aaaci[langue])

    texte_paramère=Label(fênetre_paramétre, text=trad_aaacj[langue])
    texte_paramère.pack()
    if langue=="fr":
        langue_séléction=StringVar(value="Français")
    else:
        langue_séléction=StringVar(value="English")
    liste_découlante_langue=ttk.Combobox(fênetre_paramétre, values=["English","Français"], state="readonly", textvariable=langue_séléction)
    liste_découlante_langue.pack()

    bouton_valider=Button(fênetre_paramétre, text=trad_jaaaa[langue], command=valider).pack()

    fênetre_paramétre.grab_set()
    fênetre_paramétre.wait_window()


def éditeur_PyCreator():
    """Fonction principale de PyCreator"""
    apliquer_les_paramètre() # on met a jour les paramètre a l'ouverture
    global fichier

    fichier=[{"documentation":"", "variables":[]}]

    global documentation_entrée_texte

    def export():
        """Cette fonction appellèle l'autre fonciton d'export pour avoir l'argument."""
        global fichier
        fichier[0]["documentation"]=documentation_entrée_texte.get()
        
        exporter_le_programme(fichier_liste=fichier, langue_pour_gestionaire_de_fichier=langue)
    
    def enregister_le_fichier_fênetre():
        """Cette fonciton appèle l'autre fonction d'export pour avoir l'argument."""
        fichier[0]["documentation"]=documentation_entrée_texte.get()
        
        enregistrer_le_fichier(liste_fichier=fichier, langue_pour_gestionaire_de_fichier=langue)
    
    def ouvrir_le_fihcier_fênetre():
        """Cette fonction appèlle l'autre fonction d'ouverture pour avoir le retour"""
        global fichier
        fichier_tmp_pour_ouverture=ouvrir_un_fichier_PPyC(langue_pour_gestionaire_de_fichier=langue)

        if fichier_tmp_pour_ouverture!="Annuler":
            fichier=fichier_tmp_pour_ouverture
            mise_a_jours_interface_graphique()
    
    def paramètre():
        """Cette fonction apèle la fonction de paramètra pour odnné l'argument"""
        modifier_les_paramètre(fênetre="éditeur")

    def action_pour_bouton_supprimer_variable():
        """Cette fonction est appelé par le boutton de supprésion de varaible.
        Il ouvre une fênetre d'avertissement que si la variable est en cours d'utilisation, cela causera des erreures."""
        def valider_bouton():
            """Cette fonction est appelé par la bouton.
            Elle confirme la suppression de la variable.
            La variable est donc supprimé, et la listbox est mise a jour."""
            avertissement_suppresion_de_variable.destroy()
            index_varaible_à_supprimer=liste_des_variable_graphique.curselection()[0]

            # suppression dans la fichier :
            del fichier[0]["variables"][index_varaible_à_supprimer]
            
            liste_des_variable_graphique.delete(liste_des_variable_graphique.curselection())
            
            logging.debug(fichier[0]["variables"])
        
        avertissement_suppresion_de_variable=Toplevel(fênetre_éditeur_PyCreator)
        avertissement_suppresion_de_variable.title(trad_aaaff[langue])

        texte_aversissement=Label(avertissement_suppresion_de_variable, text=trad_aaafg[langue]).pack()

        bouton_annuler=Button(avertissement_suppresion_de_variable, text=trad_jaaaf[langue], command=avertissement_suppresion_de_variable.destroy).pack()

        bouton_valider=Button(avertissement_suppresion_de_variable, text=trad_jaaaa[langue], command=valider_bouton).pack()

        avertissement_suppresion_de_variable.grab_set()
        avertissement_suppresion_de_variable.wait_window()

    

    global fênetre_éditeur_PyCreator
    global espace_de_code
    global code_frame

    fênetre_éditeur_PyCreator=Tk()
    fênetre_éditeur_PyCreator.title(trad_aaaaa[langue])

    fênetre_éditeur_PyCreator.geometry("800x600")

    barre_menu_liste_déroulant = Menu(fênetre_éditeur_PyCreator)
    fênetre_éditeur_PyCreator.config(menu=barre_menu_liste_déroulant)

    menu_fichier = Menu(barre_menu_liste_déroulant, tearoff=0)
    barre_menu_liste_déroulant.add_cascade(label=trad_aaaab[langue], menu=menu_fichier)

    menu_fichier.add_command(label=trad_aaaac[langue], command=ouvrir_le_fihcier_fênetre)

    menu_fichier.add_command(label=trad_aaaad[langue], command=enregister_le_fichier_fênetre)

    menu_fichier.add_command(label=trad_aaaae[langue], command=export)

    menu_PyCreator = Menu(barre_menu_liste_déroulant, tearoff=0)

    barre_menu_liste_déroulant.add_cascade(label=trad_jaaae[langue], menu=menu_PyCreator)

    menu_PyCreator.add_command(label=trad_aaaci[langue], command=paramètre)

    # valeur -------------------------------

    valeur_frame=LabelFrame(fênetre_éditeur_PyCreator, text=trad_aaadh[langue])

    # les variable

    variable_frame=LabelFrame(valeur_frame, text=trad_aaadg[langue])

    global liste_des_variable_graphique

    listbox_frame = Frame(variable_frame)

    liste_des_variable_graphique=Listbox(listbox_frame)

    scrollbar_variable = Scrollbar(listbox_frame, orient=VERTICAL)

    liste_des_variable_graphique.config(yscrollcommand=scrollbar_variable.set)
    scrollbar_variable.config(command=liste_des_variable_graphique.yview)

    liste_des_variable_graphique.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar_variable.pack(side=RIGHT, fill=Y)

    listbox_frame.grid(column=0, columnspan=2, row=0)


    texte_information_varaible=Label(variable_frame, text=trad_aaafe[langue]).grid(column=0, columnspan=2, row=1)

    bouton_ajouter_une_variable=Button(variable_frame, text=trad_aaadi[langue], command=crée_une_variable).grid(column=0, row=2)

    bouton_supprimer_une_variable=Button(variable_frame, text=trad_aaafd[langue], command=action_pour_bouton_supprimer_variable)
    bouton_supprimer_une_variable.grid(column=1, row=2)

    variable_frame.pack()

    valeur_frame.grid(column=0, row=0, rowspan=2, padx=5)
    
    def controle_de_séléction_de_liste():
        """Cette fonction est appelé en permanance dans la mainloop.
        Elle permet de controler qu'un élément est séléctionner dans la listebox qui contient les variable, et de griser le bouton 'supprimer' si aucun élément est séléctionner dans la listebox."""
        if liste_des_variable_graphique.curselection()==():     # si la condition est vrai, aucun élément de la liste est séléctionner.
            bouton_supprimer_une_variable["state"] = "disabled"

        else:
            bouton_supprimer_une_variable["state"] = "normal"
        
        fênetre_éditeur_PyCreator.after(temps_de_mise_a_jour_interface_graphique, controle_de_séléction_de_liste)

    controle_de_séléction_de_liste()
    
    # espace de code -----------------------------------

    conteneur_espace_code = Frame(fênetre_éditeur_PyCreator)

    global canvas_code, scrollbar_code

    canvas_code = Canvas(conteneur_espace_code, width=200, height=400)

    scrollbar_code = Scrollbar(conteneur_espace_code, orient=VERTICAL, command=canvas_code.yview)

    canvas_code.configure(yscrollcommand=scrollbar_code.set)

    espace_de_code=LabelFrame(canvas_code, text=trad_aaaaf[langue])

    canvas_window = canvas_code.create_window((0, 0), window=espace_de_code, anchor="nw")

    canvas_code.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar_code.pack(side=RIGHT, fill=Y)

    code_frame=LabelFrame(espace_de_code, text=trad_aaaag[langue])
    ajouter_une_ligne_bouton=Button(code_frame, text=trad_aaaah[langue], command=ajouter_une_ligne).pack()

    conteneur_espace_code.grid(column=1, row=0, rowspan=3, padx=5, sticky="new")

    code_frame.pack()

    def configurer_scroll_region(event=None):
        canvas_code.configure(scrollregion=canvas_code.bbox("all"))

    # Binding pour mettre à jour la région de scroll quand le contenu change
    espace_de_code.bind("<Configure>", configurer_scroll_region)

    # Permet le défilement avec la molette de la souris
    def _on_mousewheel(event):
        canvas_code.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas_code.bind_all("<MouseWheel>", _on_mousewheel)

    # documentation du projet ------------------------------

    documentation_frame=LabelFrame(fênetre_éditeur_PyCreator, text=trad_aaade[langue])
    texte_documentation_frame=Label(documentation_frame, text=trad_aaadf[langue]).pack()
    
    documentation_entrée_texte=Entry(documentation_frame, width=60)
    documentation_entrée_texte.pack()

    documentation_frame.grid(column=2, row=0, padx=5, sticky="nsew")

    def mise_a_jour_dans_le_fichier_la_doc():
        """Cette fonction est applé a chaque modification de la documentation, pour enregistrer les modification dans le fichier."""
        fichier[0]["documentation"]=documentation_entrée_texte.get()
        fênetre_éditeur_PyCreator.after(temps_de_mise_a_jour_interface_graphique, mise_a_jour_dans_le_fichier_la_doc)

    mise_a_jour_dans_le_fichier_la_doc()

    mise_a_jours_interface_graphique()

    mise_a_jour_canva()

    fênetre_éditeur_PyCreator.mainloop()

fênetre_ajouter_une_ligne=None

valeur_tmp=None
fênetre_ajouter_une_ligne_ecrire_dans_le_terminale=None
fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique=None

def crée_une_variable():
    """Cette fonction crée une variable."""
    def valider_la_variable():
        """Cette fonction est appelé quand l'utilisateur clique sur le bouton valider.
        Cela ouvre une fênetre pour définire la valeur par défaut.
        """
        def action_pour_le_bouton_non():
            """Cette fonction est apelé par le bouton 'non'. Elle met donc la valeur par défaut de la variable à None."""
            variable_tmp["Valeur"]="None"
            fênetre_valeur_par_défaut.destroy()
            fichier[0]["variables"].append({"Nom":variable_tmp["Nom"], "Valeur par défaut":variable_tmp["Valeur"]})
            # Ajouter la nouvelle variable à la liste box
            liste_des_variable_graphique.insert(END, variable_tmp["Nom"])

        def action_pour_le_bouton_oui():
            """Cette fonction est apelé par la bouton 'oui'. Elle permet de mettre la valeur par défaut à une valeur choisis pas l'utilisateur."""
            def définire_la_valeur():
                """Cette fonction va ouvrire la fênetre de valeur, puis utiliser la variable valeur_tmp pour mettre la valeur par défaut de la variable."""
                ajouter_une_valeur()
            
                valeur_pour_variable_tmp=valeur_tmp
                logging.debug("Valeur pour variable : " + valeur_pour_variable_tmp)
                valeur_du_texte.set(trad_aaabe[langue] + str(valeur_pour_variable_tmp))


            def action_pour_validé():
                """Cette fonction est appelé par le bouton valider. Il permet de mettre toutes les information sur la variable dans 'variable_tmp'"""
                variable_tmp["Valeur"]=valeur_tmp

                chois_de_la_valeur_par_défaut_fênetre.destroy()
                fênetre_valeur_par_défaut.destroy()

                fichier[0]["variables"].append({"Nom":variable_tmp["Nom"], "Valeur par défaut":variable_tmp["Valeur"]})
                # Ajouter la nouvelle variable à la liste box
                liste_des_variable_graphique.insert(END, variable_tmp["Nom"])

            chois_de_la_valeur_par_défaut_fênetre=Toplevel(fênetre_valeur_par_défaut)
            chois_de_la_valeur_par_défaut_fênetre.title(trad_aaafb[langue])

            teste_chois_de_la_valeur=Label(chois_de_la_valeur_par_défaut_fênetre, text=trad_aaafc[langue]).pack()

            frame_valeur=LabelFrame(chois_de_la_valeur_par_défaut_fênetre, text=trad_aaabh[langue])
            définire_la_valeur_bouton=Button(frame_valeur, text=trad_jaaab[langue], command=définire_la_valeur).pack()
            valeur_du_texte = StringVar()
            valeur_du_texte.set(trad_aaabi[langue])
            valeur_texte=Label(frame_valeur, textvariable=valeur_du_texte)
            valeur_texte.pack()
            frame_valeur.pack()
            valider=Button(chois_de_la_valeur_par_défaut_fênetre, text=trad_jaaaa[langue], command=action_pour_validé).pack()

            chois_de_la_valeur_par_défaut_fênetre.grab_set()
            chois_de_la_valeur_par_défaut_fênetre.wait_window()


        variable_tmp={"Nom":"", "Valeur":""}

        variable_tmp["Nom"]=chan_texte_nom_de_variable.get()

        fênetre_crée_variable.destroy()

        fênetre_valeur_par_défaut=Toplevel(fênetre_éditeur_PyCreator)
        fênetre_valeur_par_défaut.title(trad_aaadi[langue])

        texte_valeur_défaut_variable=Label(fênetre_valeur_par_défaut, text=trad_aaaea[langue]).pack()

        # bouton oui/non :

        bouton_non=Button(fênetre_valeur_par_défaut, text=trad_jaaag[langue], command=action_pour_le_bouton_non).pack()
        bouton_oui=Button(fênetre_valeur_par_défaut, text=trad_jaaah[langue], command=action_pour_le_bouton_oui).pack()

        fênetre_valeur_par_défaut.grab_set()
        fênetre_valeur_par_défaut.wait_window()
    
    def controle_nom_de_la_varaible():
        """Cette fonction est appelé dans la mainloop.
        Elle controle le nom de la variable avec plusieurs point :
        - caractère interdit (et espace)
        - nom déjà utiliser
        - nom vide
        et des avertissement :
        - caractère accentué
        - underscore en début ou en fin
        """
        def controle():
            """Cette variable effectue le controle et fait un return dès qu'il y a une erreur"""
            def désactiver_le_bouton():
                """Cette fonction désactive le bouton ("disabled"), ce qui fait que l'utilisateur ne peut plus cliquer dessus.
                Cette fonction désactive aussi les avertissement"""
                bouton_valider["state"] = "disabled"
                texte_avertisement_stringvar.set("")
            
            nom_variable_tmp=chan_texte_nom_de_variable.get()
            # controle d'erreur :

            # controle du nom vide :
            if nom_variable_tmp=="":    # le nom de la variable est vide
                texte_erreur_stringvar.set(trad_aaage[langue])
                désactiver_le_bouton()
                return None

            # controle de caractère
            for caractère in nom_variable_tmp:
                if not (caractère.isalpha() or caractère == "_"):       # contient un caractère interdit
                    texte_erreur_stringvar.set(trad_aaagd[langue])
                    désactiver_le_bouton()
                    return None

            # teste si le nom existe déjà :
            liste_tmp_variable=[]
            for élement in fichier[0]["variables"]:
                liste_tmp_variable.append(élement["Nom"])

            if nom_variable_tmp in liste_tmp_variable:      # contorle si la variable en cours de création existe déjà
                texte_erreur_stringvar.set(trad_aaagf[langue])
                désactiver_le_bouton()
                return None
                
            # si les controle précédent n'on pas retourné None, c'est qu'il n'y a pas d'erreur sur le nom de variable.
            texte_erreur_stringvar.set("")  # suppréssion du potentiel texte

            bouton_valider["state"] = "normal"
            avertissement()

        def avertissement():
            """Cette fonction gère les avertissement :
            - nom de variable contenant des accent
            - nom de variable contenant des _ au début
            un avertissement ne bloc pas la création de la variable, mais le déconseil.
            """
            nom_variable_tmp=chan_texte_nom_de_variable.get()
            def contient_des_accent(caractère):
                """Cette fonction recoit en argument une chaine de caractère et returne True si un des caractère contient un accent et False si il n'en contient pas."""
                return not(bool(re.fullmatch(r"[A-Za-z_]+", caractère)))
                
            texte_avertissement_tmp=""

            # les avertissement : quand il y a un avertissement, l'utilisateur peut crée la variable mais il est fortement déconseiller de ne pas le faire.
            if contient_des_accent(caractère=nom_variable_tmp):
                texte_avertissement_tmp = trad_aaagh[langue]

            if len(nom_variable_tmp)!=0:      # vérification que la chaine de caractère n'est pas vide pour éviter l'erreur IndexError: string index out of range
                if nom_variable_tmp[0]=="_":        # avertissement que le nom peut être utiliser pour un nom spécial réservé
                    texte_avertissement_tmp = texte_avertissement_tmp + trad_aaagi[langue]
            
            texte_avertisement_stringvar.set(texte_avertissement_tmp)
            

        controle()
        

        fênetre_crée_variable.after(temps_de_mise_a_jour_interface_graphique, controle_nom_de_la_varaible)



    fênetre_crée_variable=Toplevel(fênetre_éditeur_PyCreator)

    fênetre_crée_variable.title(trad_aaadi[langue])

    texte_création_de_variable=Label(fênetre_crée_variable, text=trad_aaadj[langue]).grid(column=0, columnspan=2, row=0)
    
    texte_erreur_stringvar=StringVar()
    texte_erreur_stringvar.set("")

    texte_avertisement_stringvar=StringVar()
    texte_avertisement_stringvar.set("")

    texte_erreur_label=Label(fênetre_crée_variable, textvariable=texte_erreur_stringvar, fg="red")
    texte_erreur_label.grid(column=0, columnspan=2, row=2)

    texte_avertissement_label=Label(fênetre_crée_variable, textvariable=texte_avertisement_stringvar, fg="#DFBF0C")
    texte_avertissement_label.grid(column=0, columnspan=2, row=3)

    chan_texte_nom_de_variable=Entry(fênetre_crée_variable)
    chan_texte_nom_de_variable.grid(column=0, row=4, columnspan=2)

    bouton_valider=Button(fênetre_crée_variable, text=trad_jaaaa[langue], command=valider_la_variable)
    bouton_valider.grid(column=0, row=5)
    bouton_annuler=Button(fênetre_crée_variable, text=trad_jaaaf[langue], command=fênetre_crée_variable.destroy).grid(column=1, row=5)

    controle_nom_de_la_varaible()

    fênetre_crée_variable.grab_set()
    fênetre_crée_variable.wait_window()
    

def ajouter_une_valeur():
    """Cette fonction est appelé pour ajouter une valeur. Elle ouvre une fênetre avec des bouton pour choisire quelle valeur il veut."""
    def chaine_str():
        """Cette fonction permet la définition d'une chaine de caractère."""
        def valider_str():
            """Cette fonction est appelé quand l'utilisateur clique sur validé"""
            global valeur_tmp
            valeur_tmp=chan_texte.get()
            valeur_tmp="'" + valeur_tmp + "'"
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

    def valeur_variable():
        """Cette fonction ouvre la fênetre pour choisire quelle variable l'utilisateur utilise la valeur."""
        fênetre_valeur.destroy()

        def valider_mise_valeur_variable():
            """Cette fonction est appelé par le bouton 'valider'. Cela controle que l'utilisateur ai bien séléctionner une variable. Ensuite, la valeur est mise dans la variable 'valeur_tmp'."""
            nom_variable_tmp=liste_déroulante_variable.get()

            if nom_variable_tmp=="":        # l'utilisateur n'a pas sésit de variable.
                erreur_saisit_de_variable=Toplevel(fênetre_valeur_variable)
                erreur_saisit_de_variable.title(trad_aaaeh[langue])

                texte_erreur_saisit_de_variable=Label(erreur_saisit_de_variable, text=trad_aaaei[langue]).pack()

                bouton_ok_erreur_varaible=Button(erreur_saisit_de_variable, text=trad_jaaai, command=erreur_saisit_de_variable.destroy).pack()

                erreur_saisit_de_variable.grab_set()
                erreur_saisit_de_variable.wait_window()

            else:
                global valeur_tmp

                valeur_tmp=nom_variable_tmp
                fênetre_valeur_variable.destroy()

        if fichier[0]["variables"]==[]:     # pas de variables
            fênetre_erreur_pas_de_variable=Toplevel(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique)
            fênetre_erreur_pas_de_variable.title(trad_aaaef[langue])
            texte_erreur_variable=Label(fênetre_erreur_pas_de_variable, text=trad_aaafa[langue]).pack()
            bouton_ok=Button(fênetre_erreur_pas_de_variable, text=trad_jaaai[langue], command=fênetre_erreur_pas_de_variable.destroy).pack()
            fênetre_erreur_pas_de_variable.grab_set()
            fênetre_erreur_pas_de_variable.wait_window()

        else:
            fênetre_valeur_variable=Toplevel(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique)
            fênetre_valeur_variable.title(trad_aaaej[langue])

            liste_variable_tmp=[]

            for element in fichier[0]["variables"]:
                liste_variable_tmp.append(element["Nom"])

            frame_choi_variable=LabelFrame(fênetre_valeur_variable, text=trad_aaaee[langue])
            liste_déroulante_variable=ttk.Combobox(frame_choi_variable, values=liste_variable_tmp, state="readonly")
            liste_déroulante_variable.pack()
            frame_choi_variable.pack()

            bouton_valider=Button(fênetre_valeur_variable, text=trad_jaaaa[langue], command=valider_mise_valeur_variable).pack()

            fênetre_valeur_variable.grab_set()
            fênetre_valeur_variable.wait_window()


    global fênetre_ajouter_une_ligne_ecrire_dans_le_terminale

    fênetre_valeur=Toplevel(fênetre_ajouter_une_ligne_ecrire_dans_le_terminale)
    fênetre_valeur.title(trad_aaaba[langue])
    fênetre_valeur.grab_set()
    texte_fênetre_valeur=Label(fênetre_valeur, text=trad_aaabb[langue]).pack()

    frame_valeurs_littérales=LabelFrame(fênetre_valeur, text=trad_aaabc[langue])
    bouton_str=Button(frame_valeurs_littérales, text=trad_aaabd[langue], command=chaine_str).pack()
    frame_valeurs_littérales.pack()

    frame_variable=LabelFrame(fênetre_valeur, text=trad_aaadg[langue])

    bouton_valeur_de_la_variable=Button(frame_variable, text=trad_aaaej[langue], command=valeur_variable).pack()

    frame_variable.pack()

    fênetre_valeur.wait_window()

valeur_texte=None
def ajouter_une_ligne():
    """Cette fonction gère l'ajout d'une ligne de code"""
    logging.debug("Ajouter une ligne")
    def bouton_print():
        """Cette fonction est apelé quand l'utilisateur clique sur le bouton print."""
        def définire_la_valeur():
            """Cette fonction définit la valeur du print"""
            ajouter_une_valeur()
            
            valeur_pour_print=valeur_tmp
            logging.debug("Valeur pour print : " + valeur_pour_print)
            valeur_du_texte.set(trad_aaabe[langue] + str(valeur_pour_print))
        def valider():
            """Cette fonction valide le print"""
            ligne_de_code_tmp=f"print({valeur_tmp})"
            fichier.append({"humain":{"fr":f"Ecrire dans le terminale {valeur_tmp}", "en":f"Write in the terminal {valeur_tmp}"}, "Python":ligne_de_code_tmp, "type":"action"})
            logging.debug("fichier : " + str(fichier))
            fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.destroy()
            mise_a_jours_interface_graphique()

        global valeur_tmp
        valeur_tmp=""

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
    
    def bouton_mettre_variable_valeur():
        """Cette fonction permet de géré la fênetre pour la mise à une valeur d'une variable."""
        def définire_la_valeur():
            """Cette fonction définit la valeur du print"""
            ajouter_une_valeur()
            
            valeur_pour_print=valeur_tmp
            logging.debug("Valeur pour print : " + valeur_pour_print)
            valeur_du_texte.set(trad_aaabe[langue] + str(valeur_pour_print))
        
        def valider():
            """Cette fonction valide le print"""
            nom_variable_tmp=liste_déroulante_variable.get()
            if nom_variable_tmp=="":             # l'utilisateur n'a pas sésit de variable
                logging.debug("l'utilisateur n'a pas césit de variable")
                erreur_variable_nom=Toplevel(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique)
                erreur_variable_nom.title(trad_aaaeh[langue])
                texte_erreur_variable_séléction=Label(erreur_variable_nom, text=trad_aaaei[langue]).pack()

                bouton_valider=Button(erreur_variable_nom, text=trad_jaaai[langue], command=erreur_variable_nom.destroy).pack()

                erreur_variable_nom.grab_set()
                erreur_variable_nom.wait_window()

            else:
                ligne_de_code_tmp=f"{nom_variable_tmp} = {valeur_tmp}"
                fichier.append({"humain":{"fr":f"Mettre la variable {nom_variable_tmp} à {valeur_tmp}", "en":f"Set the variable {nom_variable_tmp} to {valeur_tmp}"}, "Python":ligne_de_code_tmp, "type":"action"})
                logging.debug("fichier : " + str(fichier))
                fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.destroy()
                mise_a_jours_interface_graphique()

        # controle qu'il y ai bien des variable :

        if fichier[0]["variables"]==[]:     # pas de variables
            fênetre_erreur_pas_de_variable=Toplevel(fênetre_éditeur_PyCreator)
            fênetre_erreur_pas_de_variable.title(trad_aaaef[langue])
            texte_erreur_variable=Label(fênetre_erreur_pas_de_variable, text=trad_aaaeg[langue]).pack()
            bouton_ok=Button(fênetre_erreur_pas_de_variable, text=trad_jaaai[langue], command=fênetre_erreur_pas_de_variable.destroy).pack()
            fênetre_erreur_pas_de_variable.grab_set()
            fênetre_erreur_pas_de_variable.wait_window()

        else:
            global valeur_tmp
            valeur_tmp=""
            
            global valeur_texte
            global fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique
            valeur_pour_print=None
            global fênetre_ajouter_une_ligne
            fênetre_ajouter_une_ligne.destroy()

            fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique=Toplevel(fênetre_éditeur_PyCreator)
            fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.grab_set()

            fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.title(trad_aaaec[langue])

            texte_fênetre_variable=Label(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_aaaed[langue]).pack()

            frame_choi_variable=LabelFrame(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_aaaee[langue])
            liste_variable_tmp=[]

            for element in fichier[0]["variables"]:
                liste_variable_tmp.append(element["Nom"])
            
            liste_déroulante_variable=ttk.Combobox(frame_choi_variable, values=liste_variable_tmp, state="readonly")
            liste_déroulante_variable.pack()
            frame_choi_variable.pack()

            frame_valeur=LabelFrame(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_aaabh[langue])
            définire_la_valeur=Button(frame_valeur, text=trad_jaaab[langue], command=définire_la_valeur).pack()
            valeur_du_texte = StringVar()
            valeur_du_texte.set(trad_aaabi[langue])
            valeur_texte=Label(frame_valeur, textvariable=valeur_du_texte)
            valeur_texte.pack()
            frame_valeur.pack()
            valider=Button(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_jaaaa[langue], command=valider).pack()
    
    def ajouter_un_commentaire_bouton():
        """Cette fonction est applé par la bouton ajouter un commentaire.
        Cette fonction ouvre ensuite une fêntre pour que l'utilisateur sésice sont commentaire."""
        def valider_le_commentaire_bouton():
            """Cette fonction est applé par le bouton valider.
            Il crée le commentaire."""
            commentaire_tmp=entré_texte_pour_commmentaire.get()
            fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.destroy()

            fichier.append({"humain":{"fr":commentaire_tmp, "en":commentaire_tmp}, "Python":f"#{commentaire_tmp}", "type":"commentaire"})
            mise_a_jours_interface_graphique()


        fênetre_ajouter_une_ligne.destroy()

        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique=Toplevel(fênetre_éditeur_PyCreator)
        
        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.title(trad_aaafj[langue])

        texte_fênetre_variable=Label(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_aaaga[langue]).grid(column=0, columnspan=2, row=0)

        entré_texte_pour_commmentaire=Entry(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, width=50)
        entré_texte_pour_commmentaire.grid(column=0, columnspan=2, row=1)

        bouton_valider=Button(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_jaaaa[langue], command=valider_le_commentaire_bouton).grid(column=0, row=2)

        bouton_annuler=Button(fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique, text=trad_jaaaf[langue], command=fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.destroy).grid(column=1, row=2)

        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.grab_set()
        fênetre_ajouter_une_ligne_fonction_de_fenetre_graphique.wait_window()

    global fênetre_ajouter_une_ligne

    fênetre_ajouter_une_ligne = Toplevel(fênetre_éditeur_PyCreator)
    fênetre_ajouter_une_ligne.grab_set()
    fênetre_ajouter_une_ligne.title(trad_jaaac[langue])


    frame_commande_pyhton=LabelFrame(fênetre_ajouter_une_ligne, text=trad_aaabj[langue])
    frame_variable=LabelFrame(fênetre_ajouter_une_ligne, text=trad_aaadg[langue])
    frame_commentaire=LabelFrame(fênetre_ajouter_une_ligne, text=trad_aaafi[langue])


    # bouton pour les fonction python :
    bouton_ajouter_comande_print=Button(frame_commande_pyhton, text=trad_aaaca[langue], command=bouton_print).pack()
    
    # bouton pour les variables :
    bouton_ajouter_command_changer_la_valeur_d_une_variable=Button(frame_variable, text=trad_aaaeb[langue], command=bouton_mettre_variable_valeur).pack()
    
    # bouton pour les commentaire :
    bouton_ajouter_un_commentaire=Button(frame_commentaire, text=trad_aaafh[langue], command=ajouter_un_commentaire_bouton).pack()

    frame_commande_pyhton.grid(column=0, row=0, padx=5, pady=5)
    frame_variable.grid(column=1, row=0, padx=5, pady=5)

    frame_commentaire.grid(column=2, row=0, padx=5, pady=5)
    
    
def mise_a_jours_interface_graphique():
    """Cette fonction permet de metre a jours l'interface graphique, donc d'ajouter / supprimer des lignes de code."""
    def ajouter_ligne_de_code_interface(élément_utiliser:int):
        """Cette fonction ajoute a l'interface graphique un ligne de code."""
        if élément_utiliser["type"]=="action":
            nouvelle_ligne_de_code=LabelFrame(code_frame, text=trad_jaaad[langue])
        elif élément_utiliser["type"]=="commentaire":
            nouvelle_ligne_de_code=LabelFrame(code_frame, text=trad_aaagc[langue])
        else:
            logging.error("Erreur dans le fichier, pour l'élément : " + str(élément_utiliser))
            return None
        
        texte_humain=Label(nouvelle_ligne_de_code, text=élément_utiliser["humain"][langue]).pack()
        texte_python=Label(nouvelle_ligne_de_code, text=élément_utiliser["Python"]).pack()
        nouvelle_ligne_de_code.pack(padx=5, pady=5)

    global code_frame
    
    code_frame.destroy()
    code_frame=LabelFrame(espace_de_code, text=trad_aaacb[langue])

    # mise a jour des variables :

    liste_des_variable_graphique.delete(0, END)

    for element_variable in fichier[0]["variables"]:
        liste_des_variable_graphique.insert(END, element_variable["Nom"])

    # mise a jour des action

    ajout_des_action=fichier[1:len(fichier)]
    logging.debug("Fichier mis a jour : " + str(fichier))
    logging.debug("Ajout des action : " + str(ajout_des_action))
    for element in ajout_des_action:
        ajouter_ligne_de_code_interface(element)
    


    documentation_entrée_texte.delete(0, END)
    
    logging.debug("Documentation du projet : " + fichier[0]["documentation"])
    documentation_entrée_texte.insert(0, fichier[0]["documentation"])

    ajouter_une_ligne_bouton=Button(code_frame, text=trad_aaacc[langue], command=ajouter_une_ligne).pack()
    code_frame.pack(padx=10, pady=10)

    
    
def mise_a_jour_canva():
    """Cette fonction met a jour le canva en fonction de l'espace. Le canva est donc agrandis ou rétrécis en fonction de la taille de la fênetre et en fonction de la taille du code."""
    # Mise à jour de la région de scroll après l'ajout des éléments
    espace_de_code.update_idletasks()

    hauteur_nésésaire = espace_de_code.winfo_reqheight()
    largeur_nésésaire = espace_de_code.winfo_reqwidth()

    nouvelle_largeure_canva = largeur_nésésaire

    nouvelle_hauteur_canva = min(hauteur_nésésaire, fênetre_éditeur_PyCreator.winfo_height())
    canvas_code.config(height=nouvelle_hauteur_canva, width=nouvelle_largeure_canva)

    canvas_code.configure(scrollregion=canvas_code.bbox("all"))
    
    fênetre_éditeur_PyCreator.after(temps_de_mise_a_jour_interface_graphique, mise_a_jour_canva)
