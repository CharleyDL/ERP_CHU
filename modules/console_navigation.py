#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import sys

from os import system

import modules.administration as admin
import modules.clear_db as clear_db
import modules.resident as resident
import modules.fake_resident as fake




def header() -> None:
    """Display the CHU ERP HEADER"""

    with open('./img/header.txt', 'r') as f:
        print(f.read())


def choice() -> int:
    """Get the user's choice"""

    try:
        choice = int(input("\nVotre choix : "))

    except Exception as e:
        print(e)

    return choice


def console_menu() -> int:
    """Display the console main menu"""

    system('clear')    # Clear the terminal

    # Display the header and options
    header()
    print("   -- 1 : Gérer les patients")
    print("   -- 2 : Gérer les employés")
    print("   -- 3 : Accéder aux archives")
    print("   -- 4 : Options")
    print("   -- 5 : Quitter")

    # Get the user choice
    menu_choice = choice()

    return menu_choice


def patient_ms() -> None:
    """Display the menu : Patient Management System"""

    system('clear') # Clear the terminal

    # Display the header and options
    header()
    print("   -- 1: Enregistrer un nouveau patient")
    print("   -- 2: Enregistrer une sortie")
    print("   -- 3: Effacer définitivement un patient de la base de données")
    print("   -- 4: Afficher le nombre de patients présents à l'hôpital")
    print("   -- 5: Afficher la table 'Patients'")
    print("   -- 6: Menu principal")

    menu_choice = choice() # Get the user choice
    if menu_choice == 1:
        # Get information by the user
        new_patient, date_entree = resident.create_patient()
        id_patient_archive = new_patient[0]    # get id for archive

        # Patient Instantiation and save in table patients
        new_patient = resident.Patient(*new_patient)
        resident.Patient.entrer_a_l_hopital(new_patient)

        # Save in Archive
        new_archive = admin.Archive(id_patient_archive, date_entree, None)
        admin.Archive.save_in_db(new_archive)

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 2:
        # Get information by the user
        print("\nPour rappel - id_patient : NomPrenomGrp_SanguinDate_Entree(YYYY-MM-DD)")
        identifiant_patient, date_sortie = resident.Patient.sortir_de_l_hopital(input("Entrer l'identifiant du patient : "))
        date_entree = identifiant_patient[-1:-10]   # Get the date of entry

        # Save in Archive
        update_archive = admin.Archive(identifiant_patient, date_entree, date_sortie)
        admin.Archive.save_in_db(update_archive)

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 3:
        # Get information by the user
        print("\nPour rappel - id_employe : NomPrenomGrp_SanguinDate_Entree(YYYY-MM-DD)")

        # Delete the patient
        resident.Patient.effacer_un_patient(input("Entrer l'identifiant du patient : "))

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 4:
        # Gives the number of patients in the hospital
        resident.Patient.count_patient_in_db()

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 5:
        # Display the patient table
        resident.Patient.display_table()

        input("Appuyer sur 'Entrée' pour continuer")


def rh_ms() -> None:
    """Display the menu : Employee Management System"""

    system('clear') # Clear the terminal

    # Display the header and options
    header()
    print("   -- 1: Enregistrer un nouvel employé")
    print("   -- 2: Enregister une fin de contrat (CDD-CDI)")
    print("   -- 3: Effacer définitivement un employé de la base de données")
    print("   -- 4: Afficher le nombre d'employés")
    print("   -- 5: Afficher la table 'RH'")
    print("   -- 6: Menu principal")

    # Get the user choice
    menu_choice = choice() # Get the user choice
    if menu_choice == 1:
        # Get information by the user and instiantiated the employee
        new_employee, date_recrutement = resident.create_employee()
        new_employee_archive = (new_employee[0], date_recrutement)    # get id for archive

        # Employee Instantiation and save in table rh
        new_employee = resident.RH(*new_employee)
        resident.RH.debuter_CDD_CDI(new_employee)

        # Save in Archive
        new_archive = admin.Archive(*new_employee_archive)
        admin.Archive.save_in_db(new_archive)

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 2:
        # Set the contract end date in database (table employe)
        print("\nPour rappel - id_employe : NomPrenomSalaireDate_Entree(YYYY-MM-DD)")
        identifiant_rh, date_sortie = resident.RH.quitter_CDD_CDI(input("Entrer l'identifiant de l'employé : "))
        date_entree = identifiant_rh[-1:-10]

        # Save in Archive
        update_archive = admin.Archive(identifiant_rh, date_entree, date_sortie)
        admin.Archive.save_in_db(update_archive)

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 3:
        # Get information by the user
        print("\nPour rappel - id_employe : NomPrenomSalaireDate_Entree(YYYY-MM-DD)")

        # Delete an employee in the database
        resident.RH.effacer_un_employe(input("Entrer l'identifiant de l'employé : "))

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 4:
        # Display the number of employees
        resident.RH.count_employee_in_db()

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 5:
        # Display the HR table
        resident.RH.display_table()

        input("Appuyer sur 'Entrée' pour continuer")


def archive_ms() -> None:
    """Display the menu : Archive Management System"""

    system('clear')     # Clear the terminal

    # Display the header and options
    header()
    print("   -- 1: Afficher les archives dans la console")
    print("   -- 2: Supprimer une archive")
    print("   -- 3: Menu principal")

    # Get the user choice
    menu_choice = choice()
    if menu_choice == 1:
        # Display archive in terminal
        admin.Archive.afficher_les_archives_console()

        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 2:
        # Delete an archive
        print("\nPour rappel - id_archive = identifiant du résident (Patient ou RH)")
        admin.Archive.del_an_archive(input("Entrer l'identifiant de l'archive : "))

        input("Appuyer sur 'Entrée' pour continuer")


def options_ms() -> None:
    """Display the menu : Archive Management System"""

    system('clear')     # Clear the terminal

    # Display the header and options
    header()
    print("   -- 1: Reset la base de données")
    print("   -- 2: Remplir la base de données de faux résident")
    print("   -- 3: Menu principal")

    # Get the user choice
    menu_choice = choice()
    if menu_choice == 1:
        # Reset the database
        clear_db.clear_all()

        print("   -- La base de données a été vidée")
        input("Appuyer sur 'Entrée' pour continuer")

    elif menu_choice == 2:
        # Create Fake Resident
        print("   -- Indiquer le nombre de faux résident que vous souhaitez")

        # Get the value by the user for each category
        nbr_patient = int(input("   -- Nombre de Faux Patient : "))
        nbr_employee = int(input("   -- Nombre de Faux Résident : "))

        fake_resident = fake.Fake(nbr_patient, nbr_employee)
        fake.Fake.add_fake_patient_db(fake_resident)
        fake.Fake.add_fake_employee_db(fake_resident)

        print("    -- Les faux résidents ont bien été ajoutés")

        input("Appuyer sur 'Entrée' pour continuer")


def console_erp() -> None:
    """Initiate the ERP menu"""

    while True:
        #**** MAIN MENU : choosing between terminal or web app ****#
        choice = console_menu()

        #**** PATIENT MANAGEMENT SYSTEM ****#
        if choice == 1:
            patient_ms()

        #**** HR MANAGEMENT SYSTEM ****#
        elif choice == 2:
            rh_ms()

        #**** ARCHIVES MANAGEMENT SYSTEM ****#
        elif choice == 3:
            archive_ms()

        #**** OPTIONS SYSTEM ****#
        elif choice == 4:
            options_ms()

        #**** END PROGRAM ****#
        else:
            sys.exit()