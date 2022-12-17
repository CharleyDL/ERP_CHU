#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import pandas as pd
import streamlit as st

from datetime import datetime

import config
import modules.administration as admin
import modules.clear_db as clear_db
import modules.fake_resident as fake
import modules.resident as resident


#**** CONSTANTS ****#
CONFIG = config.get_db_config()


################################################################################
############################# WEB APP STREAMLIT ################################
################################################################################

#********************************* METADATA ***********************************#

st.set_page_config( page_title = "CHU CAEN - ERP",
                    page_icon = ":hospital:",
                    layout = "wide"
)


# ---------------------------------------------------------------------------- #
#******************************** SIDEBAR NAV *********************************#

# CSS to center the logo
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 60%;
        }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar structure
with st.sidebar:
    st.image('img/logo_chu.png')
    st.markdown("<h1 style='text-align: center;'><b>~ E.R.P ~</b></h1>",
             unsafe_allow_html=True)
    st.markdown("<p style='text-align: right;'><em>v1.2022</em></p>",
             unsafe_allow_html=True)

add_sidebar = st.sidebar.selectbox('Navigation',
    ('Home', 'Patients', 'Ressources Humaines', 'Archives', 'Options'))

with st.sidebar:
    st.markdown("<p style='text-align: right;'>\
             <a href='mailto:charley.lebarbier@isen-ouest.yncrea.fr'><b>Bug Report</b></a>",
             unsafe_allow_html=True)


# ---------------------------------------------------------------------------- #
#********************************* HOME PAGE **********************************#

if add_sidebar == 'Home':
    # Header
    st.title("🏥 - BIENVENUE")

    datehour = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    st.markdown(f"""<p style='text-align: right;'><b>🗓️ - {datehour}</b></p>""", 
        unsafe_allow_html=True)

    st.markdown("----", unsafe_allow_html=True)

    # ------ #

    # General information
    st.markdown("#### Informations Générales :")
    st.markdown("####")     # vertical space

    ## Nombre de patient dans l'hopital
    count_in = resident.Patient.count_patient_in_db()
    st.markdown(f"""<p>‣‣‣‣ <b><u>{count_in}</u></b> patient(s) sont en séjour à l'hopital</p>""", unsafe_allow_html=True)

    ## Nombre d'employés sous contrat
    count_in = resident.RH.count_employee_in_db()
    st.markdown(f"""<p>‣‣‣‣ <b><u>{count_in}</u></b> employé(s) sont sous contrat (CDD-CDI)</p>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------- #
#****************************** PATIENT PAGE **********************************#

elif add_sidebar == 'Patients':
    st.title("Patients")

    # New Patient
    st.write("Nouveau Patient")
    form = st.form(key="new_patient")
    with form:
        cols = st.columns((1, 1))
        nom = cols[0].text_input("Nom :")
        prenom = cols[1].text_input("Prénom :")

        cols = st.columns(2)
        grp_sanguin = cols[0].selectbox(
            "Groupe Sanguin:", 
            ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-'], index=2
        )
        date_entree = cols[1].date_input("Date d'entrée :")

        st.markdown("----", unsafe_allow_html=True)

        cols = st.columns((2, 1, 2))
        new_submitted = cols[1].form_submit_button(label="Submit")

        identifiant_patient = nom+prenom+grp_sanguin+str(date_entree)
        new_patient = (identifiant_patient, nom, prenom, grp_sanguin)

    if new_submitted:
        # Patient Instantiation and save in table patients
        new_patient = resident.Patient(*new_patient)
        resident.Patient.entrer_a_l_hopital(new_patient)

        # Save in Archive
        new_archive = admin.Archive(identifiant_patient, date_entree, None)
        admin.Archive.save_in_db(new_archive)

        st.info("Patient enregistré")


    # ----------------- #
    # Enter an end date
    st.write("Fin de séjour")
    form = st.form(key="end_date_patient")
    with form:
        cols = st.columns((1, 1))
        identifiant_patient = cols[0].text_input("Identifiant Patient",
                placeholder="NomPrenomGrp_SanguinDate_Entree(YYYY-MM-DD)")
        date_sortie = cols[1].date_input("Date de sortie :")

        st.markdown("----", unsafe_allow_html=True)

        cols = st.columns((2, 1, 2))
        end_date_submitted = cols[1].form_submit_button(label="Submit")

    if end_date_submitted:
        resident.Patient.sortir_de_l_hopital(identifiant_patient)
        date_entree = identifiant_patient[-1:-10]    # Get the date of entry

        # Save in Archive
        update_archive = admin.Archive(identifiant_patient, date_entree, date_sortie)
        admin.Archive.save_in_db(update_archive)

        st.info("Fin de séjour enregistré")


    # ----------------- #
    # Delete one patient
    st.write("Supprimer un patient")
    form = st.form(key="del_patient")
    with form:
        identifiant_patient = st.text_input("ID Patient",
                placeholder="NomPrenomGrp_SanguinDate_Entree(YYYY-MM-DD)")

        cols = st.columns((2, 1, 2))
        del_patient = cols[1].form_submit_button(label="Submit")

    if del_patient:
        result = resident.Patient.effacer_un_patient(identifiant_patient)
        if result == True:
            st.info("Patient Supprimé")
        else:
            st.info("Vous ne pouvez pas supprimer un patient encore à l'hopital."
                + " Veuillez enregistrer sa sortie avant de le supprimer")


    # ----------------- #
    # Display the Patient Table
    expander = st.expander("Voir tous les patients")
    with expander:
        df = resident.Patient.display_table()
        st.dataframe(df)


# ---------------------------------------------------------------------------- #
#********************************* HR PAGE ************************************#

elif add_sidebar == 'Ressources Humaines':
    st.title("RH")

    # New Employee
    st.write("Nouvel Employé")
    form = st.form(key="new_employee")
    with form:
        cols = st.columns((1, 1))
        nom = cols[0].text_input("Nom :")
        prenom = cols[1].text_input("Prénom :")

        cols = st.columns(2)
        salaire = cols[0].number_input('Salaire Annuel', 0, 500000, step=100)
        date_entree = cols[1].date_input("Date d'entrée :")

        st.markdown("----", unsafe_allow_html=True)

        cols = st.columns((2, 1, 2))
        new_submitted = cols[1].form_submit_button(label="Submit")

        identifiant_employee = nom+prenom+str(salaire)+str(date_entree)
        new_employee = (identifiant_employee, nom, prenom, salaire)

    if new_submitted:
        # Patient Instantiation and save in table patients
        new_employee = resident.RH(*new_employee)
        resident.RH.debuter_CDD_CDI(new_employee)

        # Save in Archive
        new_archive = admin.Archive(identifiant_employee, date_entree, None)
        admin.Archive.save_in_db(new_archive)

        st.info("Employé enregistré")


    # ----------------- #
    # Enter an end date
    st.write("Fin de CDD - CDI")
    form = st.form(key="end_date_employee")
    with form:
        cols = st.columns((1, 1))
        identifiant_employee = cols[0].text_input("Identifiant Employee",
                placeholder="NomPrenomSalaireDate_Entree(YYYY-MM-DD)")
        date_sortie = cols[1].date_input("Date de sortie :")

        st.markdown("----", unsafe_allow_html=True)

        cols = st.columns((2, 1, 2))
        end_date_submitted = cols[1].form_submit_button(label="Submit")

    if end_date_submitted:
        resident.RH.quitter_CDD_CDI(identifiant_employee)
        date_entree = identifiant_employee[-1:-10]    # Get the date of entry

        # Save in Archive
        update_archive = admin.Archive(identifiant_employee, date_entree, date_sortie)
        admin.Archive.save_in_db(update_archive)

        st.info("Fin de contrat enregistré")


    # ----------------- #
    # Delete one employee
    st.write("Supprimer un employé")
    form = st.form(key="del_employee")
    with form:
        identifiant_employee = st.text_input("ID Employé",
                placeholder="NomPrenomSalairenDate_Entree(YYYY-MM-DD)")

        cols = st.columns((2, 1, 2))
        del_employee = cols[1].form_submit_button(label="Submit")

    if del_employee:
        result = resident.RH.effacer_un_employe(identifiant_employee)
        if result == True:
            st.info("Employé Supprimé")
        else:
            st.info("Vous ne pouvez pas supprimer un employé encore sous contrat."
                + " Veuillez enregistrer la fin de son contrat avant de le supprimer")


    # ----------------- #
    # Display the Employee Table
    expander = st.expander("Voir tous les employées")
    with expander:
        df = resident.RH.display_table()
        st.dataframe(df)


# ---------------------------------------------------------------------------- #
#******************************* ARCHIVE PAGE *********************************#

elif add_sidebar == 'Archives':
    st.title("Archives")

    col1, col2, col3 = st.columns((1, 10, 1))
    df = admin.Archive.afficher_les_archives_streamlit()
    col2.dataframe(df)


# ---------------------------------------------------------------------------- #
#********************************* OPTIONS ************************************#

elif add_sidebar == 'Options':
    st.title("Options")

    # Reset la DB
    expander = st.expander("Effacer les données de la base de données")
    with expander:
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("Patients"):
            with st.spinner("Invocation du trou noir"):
                clear_db.clear_patient_table()
                st.info("La table 'Patients' a été vidée")

        if col2.button("RH"):
            with st.spinner("Invocation du trou noir"):
                clear_db.clear_employee_table()
                st.info("La table 'RH' a été vidée")

        if col3.button("Archives"):
            with st.spinner("Invocation du trou noir"):
                clear_db.clear_archive_table()
                st.info("La table 'Archives' a été vidée")

        if col4.button("Reset All"):
            with st.spinner("Invocation du trou noir"):
                clear_db.clear_all()
                st.info("Toutes les tables ont été vidées")


    # ---------- #
    # Remplir la db en random
    expander = st.expander("Remplir la base de données de faux résidents")
    with expander:
        form = st.form(key="fake_resident")
        with form:
            nbr_patient = st.slider("Faux Patients souhaités", 0, 100)
            nbr_employee =st.slider("Faux Employés souhaités", 0, 100)

            cols = st.columns((2, 1, 2))
            fake_submitted = cols[1].form_submit_button(label="Submit")

        if fake_submitted:
            with st.spinner("En train de jouer à Dieu"):
                fake_resident = fake.Fake(nbr_patient, nbr_employee)
                fake.Fake.add_fake_patient_db(fake_resident)
                fake.Fake.add_fake_employee_db(fake_resident)

            st.info("Les faux résidents ont bien été ajoutés")