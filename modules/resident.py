#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import mysql.connector as mysqlco
import pandas as pd

from datetime import datetime
from mysql.connector import Error
from typing import Union

import config


#**** CONSTANTS ****#
CONFIG = config.get_db_config()




# Get information about patient or employee before their instantiation
def create_patient() -> Union[tuple, str]:
    """Request patient information to initiate the Class"""

    print('\n')
    patient = dict(
                    nom = input("Nom : "),
                    prenom = input("Prenom : "),
                    grp_sanguin = input("Groupe Sanguin : "),
                    date_entree = input("Date d'entree - YYYY-MM-DD : ")
                  )

    # Create the variable identifiant_patient with all entries
    identifiant_patient = map(patient.get,
            ['nom', 'prenom', 'grp_sanguin', 'date_entree'])
    identifiant_patient = ''.join(str(x) for x in identifiant_patient)
    
    # Drop and keep 'date_entree' into variable
    # And transform the patient values into tuple
    date_entree = patient.get('date_entree')
    del patient['date_entree']
    patient = tuple(patient.values())

    # Return identifiant_patient and patient values
    return (identifiant_patient, *patient), date_entree


def create_employee() -> Union[tuple, str]:
    """Request employee information to initiate the Class"""

    print('\n')
    employee = dict(
                    nom = input("Nom : "),
                    prenom = input("Prenom : "),
                    salaire = input("Salaire : "),
                    date_recrutement = input("Date de recrutement YYYY-MM-DD : ")
                )

    # Create the variable identifiant_patient with all entries
    identifiant_rh = map(employee.get,
            ['nom', 'prenom', 'salaire', 'date_recrutement'])
    identifiant_rh = ''.join(str(x) for x in identifiant_rh)

    # Drop and keep'date_entree' into variable
    # And transform the patient values into tuple
    date_recrutement = employee.get('date_recrutement')
    del employee['date_recrutement']
    employee = tuple(employee.values())

    # Return the dictionary values into a tuple
    return (identifiant_rh, *employee), date_recrutement




class Patient:
    """
    Class to create Patient and manage it
    Functions : entrer_a_l_hopital ; sortir_de_l_hopital ;
    effacer_un_patient ; count_patients_in_db ; display_table
    """

    def __init__(self, identifiant_patient, nom:str, prenom:str, 
                 groupe_sanguin:str, is_in_hospital=0) -> None:
        """
        Constructor Class Patient :
        /!\ identifiant_patient is a concatenation of : nom + prenom +
        groupe_sanguin + date_entree -> PRIMARY KEY in SQL table
        """

        # identifiant_patient(nom + prenom + groupe_sanguin + date_entree)
        self.identifiant_patient = identifiant_patient
        self.nom = nom
        self.prenom = prenom
        self.groupe_sanguin = groupe_sanguin
        self.is_in_hospital = is_in_hospital


    def entrer_a_l_hopital(self) -> bool:
        """Incrit un patient dans la base de données (table patient)"""

        try:
            # Change statut is_in_hospital à True
            self.is_in_hospital = 1

            #### DATABASE ####
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            sql = f"""
                   INSERT INTO patients (identifiant_patient,
                                         nom, prenom,
                                         groupe_sanguin, is_in_hospital)
                   VALUES ("{self.identifiant_patient}", "{self.nom}",
                           "{self.prenom}", "{self.groupe_sanguin}",
                           "{self.is_in_hospital}")
                   ON DUPLICATE KEY UPDATE nom = "{self.nom}",
                                        prenom = "{self.prenom}",
                                groupe_sanguin = "{self.groupe_sanguin}",
                                is_in_hospital = "{self.is_in_hospital}";
                   """
            #print(sql)

            cursor.execute(sql)
            db.commit()

            print(f"\nLe patient '{self.prenom} {self.nom}' a été enregistré.\n")

            return True

        except Exception as e:
            print(f"Error 'entrer_a_l_hopital' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def sortir_de_l_hopital(identifiant_patient) -> Union[str, datetime] | bool:
        """
        Passe le statut du patient à sortie de l'hopital (table patient)
        et récupère la date de sortie
        """

        try:
            # Récupérer la date de sortie pour les Archives
            date_sortie = datetime.now().strftime("%Y-%m-%d")

            # Passe le statut is_in_hospital à false: 0
            is_in_hospital = 0

            #### DATABASE ####
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            sql = f"""
                   UPDATE patients
                   SET is_in_hospital = "{is_in_hospital}"
                   WHERE identifiant_patient = "{identifiant_patient}";
                   """

            cursor.execute(sql)
            db.commit()

            print(f"\nLe patient sous l'id '{identifiant_patient}' est bien sorti.\n")

            return identifiant_patient, date_sortie

        except Exception as e:
            print(f"Error 'sortir_a_l_hopital' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def effacer_un_patient(identifiant_patient) -> bool:
        """Efface définitivement un patient 
        de la base de données (table Patient)"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Check if the patient is out before deleting
            sql = f"""
                   SELECT is_in_hospital
                   FROM patients
                   WHERE identifiant_patient = "{identifiant_patient}";
                   """
            cursor.execute(sql)
            result = cursor.fetchall()
            result = int(result[0][0])


            if result == 0:
                sql = f"""
                       DELETE FROM patients
                       WHERE identifiant_patient = "{identifiant_patient}"
                       """
                #print(sql)

                cursor.execute(sql)
                db.commit()

                print(f"\nLe patient à l'id '{identifiant_patient}' a bien été supprimé\n")

                return True

            else:
                print("\nVous ne pouvez pas supprimer un patient encore à l'hopital")
                print("Veuillez enregistrer sa sortie avant de le supprimer\n")

                return False

        except Exception as e:
            print(f"Error 'effacer_un_patient' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def count_patient_in_db() -> int | bool:
        """Compte les patients inscrits en base de données"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Counts the number of patients in the hospital
            sql = f"""
                   SELECT COUNT(is_in_hospital)
                   FROM patients
                   WHERE is_in_hospital = "1";
                   """
            cursor.execute(sql)
            count_in = cursor.fetchall()
            count_in = int(count_in[0][0])

            # Counts the number of patients not in the hospital
            sql = f"""
                   SELECT COUNT(is_in_hospital)
                   FROM patients
                   WHERE identifiant_patient = "0";
                   """
            cursor.execute(sql)
            count_out = cursor.fetchall()
            count_out = int(count_out[0][0])

            print(f"\nIl y a actuellement {count_in} patient(s) à l'hopital")

            return count_in     # Return only for streamlit app

        except Exception as e:
            print(f"Error 'count_patients_in_db' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def display_table() -> pd.DataFrame | bool:
        """Display the patient table inside the terminal"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Fetch the archive
            sql = f""" SELECT * FROM patients; """
            cursor.execute(sql)
            result = cursor.fetchall()

            # Transform the result in dataframe and Display it
            result_df = pd.DataFrame(result, columns=['ID Patient', 'Nom', 'Prenom', 'Grp Sanguin', "A l'hopital"])
            result_df.index = result_df.index + 1   # Get start the count to 1 and no 0

            print("\n")
            print(result_df.to_markdown(tablefmt="grid"),"\n")

            return result_df    # return only for streamlit app

        except Exception as e:
            print(f"Error 'display_table' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()




class RH:
    """
    Class to create Employee and manage it
    Functions : debuter_CDD_CDI ; quitter_CDD_CDI ;
    effacer_un_employe ; count_employee_in_db ; display_table
    """

    def __init__(self, identifiant_rh, nom:str, prenom:str, 
                 salaire:str, working_at_hospital=0) -> None:
        """
        Constructor Class Patient :
        /!\ identifiant_rh is a concatenation of : nom + prenom +
        salaire + date_recrutement -> PRIMARY KEY in SQL table
        """

        # identifiant_rh(nom+prenom+salaire+date_recrutement)
        self.identifiant_rh = identifiant_rh
        self.nom = nom
        self.prenom = prenom
        self.salaire = salaire
        self.working_at_hospital = working_at_hospital


    def debuter_CDD_CDI(self) -> bool:
        """Incrit un employé dans la base de données (table rh)"""

        # Change statut is_in_hospital à True
        self.working_at_hospital = 1

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            sql = f"""
                   INSERT INTO rh (identifiant_rh, nom, prenom, salaire, 
                                   working_at_hospital)
                   VALUES ("{self.identifiant_rh}", "{self.nom}",
                           "{self.prenom}", "{self.salaire}",
                           "{self.working_at_hospital}")
                   ON DUPLICATE KEY UPDATE
                                nom = "{self.nom}",
                                prenom = "{self.prenom}",
                                salaire = "{self.salaire}",
                                working_at_hospital = "{self.working_at_hospital}";
                   """
            #print(sql)

            cursor.execute(sql)
            db.commit()

            print(f"\nL'employé '{self.prenom} {self.nom}' a été enregistré\n")

            return True

        except Exception as e:
            print(f"Error 'debuter_CDD_CDI' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def quitter_CDD_CDI(identifiant_rh) -> Union[str, datetime] | bool:
        """
        Passe le statut de l'employé à ne travaille plus à l'hopital (table rh)
        et récupère la date de fin de contrat
        """

        try:
            # Récupérer la date de sortie pour les Archives
            date_sortie = datetime.now().strftime("%Y-%m-%d")

            # Passe le statut is_in_hospital à false: 0
            working_at_hospital = 0

            #### DATABASE ####
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            sql = f"""
                   UPDATE rh
                   SET working_at_hospital = "{working_at_hospital}"
                   WHERE identifiant_rh = "{identifiant_rh}";
                   """

            cursor.execute(sql)
            db.commit()

            print(f"\nL'employé sous l'id '{identifiant_rh}' est bien sorti.\n")
            
            return identifiant_rh, date_sortie

        except Exception as e:
            print(f"Error 'quitter_CDD_CDI' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def effacer_un_employe(identifiant_rh) -> bool:
        """
        Efface définitivement un employé de la base de données 
        (table Employé)
        """

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Check if the contract is finished before deleting
            sql = f"""
                   SELECT working_at_hospital
                   FROM rh
                   WHERE identifiant_rh = "{identifiant_rh}";
                   """
            cursor.execute(sql)
            result = cursor.fetchall()
            result = int(result[0][0])


            if result == 0:
                sql = f"""
                       DELETE FROM rh
                       WHERE identifiant_rh = "{identifiant_rh}"
                       """
                #print(sql)

                cursor.execute(sql)
                db.commit()

                print(f"\nL'employé à l'id '{identifiant_rh}' a bien été supprimé\n")

                return True

            else:
                print("\nVous ne pouvez pas supprimer un employé encore sous contrat")
                print("Veuillez enregistrer une fin de contrat avant de le supprimer\n")
                return False

        except Exception as e:
            print(f"Error 'effacer_un_employe' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def count_employee_in_db() -> int | bool:
        """Compte les employés inscrits en base de données"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Counts the number of employee working at hospital
            sql = f"""
                   SELECT COUNT(working_at_hospital)
                   FROM rh
                   WHERE working_at_hospital = "1";
                   """
            cursor.execute(sql)
            count_in = cursor.fetchall()
            count_in = int(count_in[0][0])

            # Counts the number of employee not working at hospital
            sql = f"""
                   SELECT COUNT(working_at_hospital)
                   FROM rh
                   WHERE working_at_hospital = "0";
                   """
            cursor.execute(sql)
            count_out = cursor.fetchall()
            count_out = int(count_out[0][0])


            print(f"\nIl y a actuellement {count_in} employé(s) à l'hopital")

            return count_in     #  Return only for streamlit

        except Exception as e:
            print(f"Error 'count_employee_in_db' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def display_table() -> pd.DataFrame | bool:
        """Display the rh table inside the terminal"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Fetch the archive
            sql = f"""SELECT * FROM rh;"""
            cursor.execute(sql)
            result = cursor.fetchall()

            # Transform the result in dataframe and Display it
            result_df = pd.DataFrame(result, columns=['ID Employé', 'Nom', 'Prenom', 'Salaire', 'En CDD/CDI'])
            result_df.index = result_df.index + 1    # Get start the count to 1 and no 0

            print("\n")
            print(result_df.to_markdown(tablefmt="grid"),"\n") 

            return result_df    # return only for streamlit app

        except Exception as e:
            print(f"Error 'display_table' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()