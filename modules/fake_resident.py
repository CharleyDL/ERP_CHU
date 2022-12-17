#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import datetime
import random
import names

from typing import Union

import modules.administration as admin
import modules.resident as resident




class Fake:
    """Add fake patients and employees in db"""

    def __init__(self, nbr_patient: int, nbr_employee : int) -> None:
        self.nbr_patient = nbr_patient
        self.nbr_employee = nbr_employee


    def add_fake_patient_db(self) -> None:
        """Add fake new patient"""

        for i in range(self.nbr_patient): 
            identifiant_patient, new_patient, date_entree, date_sortie = Fake.create_fake_patient()

            #**** Save in db ****#
            # Rentre le faux patient en db avec la date d'entrée
            new_patient = resident.Patient(*new_patient)
            resident.Patient.entrer_a_l_hopital(new_patient)
            new_archive = admin.Archive(identifiant_patient, date_entree, None)
            admin.Archive.save_in_db(new_archive)

            # Sort le patient et inscrit la date de sortie seulement si la date est révolue
            if date_sortie <= datetime.date.today():
                resident.Patient.sortir_de_l_hopital(identifiant_patient)
                update_archive = admin.Archive(identifiant_patient, date_entree, date_sortie)
                admin.Archive.save_in_db(update_archive)


    def add_fake_employee_db(self) -> None:
        """Add fake new employee"""

        for i in range(self.nbr_employee): 
            identifiant_employee, new_employee, date_entree, date_sortie = Fake.create_fake_employee()

            #**** Save in db ****#
            # Rentre le faux employé en db avec la date d'entrée
            new_employee = resident.RH(*new_employee)
            resident.RH.debuter_CDD_CDI(new_employee)
            new_archive = admin.Archive(identifiant_employee, date_entree, None)
            admin.Archive.save_in_db(new_archive)

            # Sort l'employé et inscrit la fin de contrat seulement si la date est révolue
            if date_sortie <= datetime.date.today():
                resident.RH.quitter_CDD_CDI(identifiant_employee)
                update_archive = admin.Archive(identifiant_employee, date_entree, date_sortie)
                admin.Archive.save_in_db(update_archive)


    @staticmethod
    def create_fake_patient() -> Union[str, datetime.date]:
        """Initiate a random patient"""

        # Nom
        nom = names.get_last_name()

        # Prenom
        prenom = names.get_first_name()

        # Grp Sanguin
        bloodtype = ['A+','A-','AB+','AB-','B+','B-','O+','O-']
        grp_sanguin=random.choice(bloodtype)

        # Début du séjour
        date_entree = datetime.date.today() - datetime.timedelta(days=random.randint(1,365))

        # Fin séjour (bridé à 90 jours max)
        date_sortie = date_entree + datetime.timedelta(days=random.randint(1,90))

        # ID patient
        identifiant_patient = nom+prenom+grp_sanguin+str(date_entree)

        # New Patient information
        new_patient = (identifiant_patient, nom, prenom, grp_sanguin)

        return identifiant_patient, new_patient, date_entree, date_sortie


    @staticmethod
    def create_fake_employee() -> Union[str, int, datetime.date]:
        """ Initiate a random patient """

        # Nom
        nom = names.get_last_name()

        # Prenom
        prenom = names.get_first_name()

        # Salaire
        salaire = random.randrange(1000, 500000, 100)

        # Début du séjour
        date_entree = datetime.date.today() - datetime.timedelta(days=random.randint(1,365))

        # Fin séjour
        date_sortie = date_entree + datetime.timedelta(days=random.randint(1,365))

        # ID patient
        identifiant_employee = nom+prenom+str(salaire)+str(date_entree)

        # New Patient information
        new_employee = (identifiant_employee, nom, prenom, salaire)

        return identifiant_employee, new_employee, date_entree, date_sortie