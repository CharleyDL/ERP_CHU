#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import mysql.connector as mysqlco
import pandas as pd

from mysql.connector import Error

import config


#**** CONSTANTS ****#
CONFIG = config.get_db_config()




class Archive:
    """Class to create and manage archive"""

    # Constructeur #
    def __init__(self, identifiant_resident, date_entree, date_sortie=None) -> None:
        self.identifiant_resident = identifiant_resident
        self.date_entree = date_entree
        self.date_sortie = date_sortie


    # Archives Management #
    def save_in_db(self) -> bool:
        """Save in archive the patient and employee for the hospital history"""

        try:
            #* DATABASE *#
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Check if identifiant_resident is already in base
            sql = f"""
                   SELECT identifiant_resident, date_sortie
                   FROM archives
                   WHERE (identifiant_resident = "{self.identifiant_resident}"
                          AND date_sortie IS NULL);
                   """
            cursor.execute(sql)
            result = cursor.fetchall()
            result = bool(result)


            if result == False:  # If the resident not in base
                sql = f"""
                       INSERT INTO archives (identifiant_resident,
                                             date_entree, date_sortie)
                       VALUES ("{self.identifiant_resident}", 
                               "{self.date_entree}", 
                               NULL);
                       """
                # print(sql)

                cursor.execute(sql)
                db.commit()

            else:  # If the resident is in base
                sql = f"""
                       UPDATE archives
                       SET date_sortie = "{self.date_sortie}"
                       WHERE identifiant_resident = "{self.identifiant_resident}";
                       """
                # print(sql)

                cursor.execute(sql)
                db.commit()

            return True

        except Exception as e:
            print(f"Error 'save_in_db' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    def del_an_archive(identifiant_resident):
        """Delete definetely an archive entry"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Check if the entry exist
            sql = f"""
                   SELECT identifiant_resident
                   FROM archives
                   WHERE identifiant_resident = "{identifiant_resident}";
                   """
            cursor.execute(sql)
            result = cursor.fetchall()
            result = bool(result)


            if result == True:
                # Confirm choice
                print("\nAttention ! Cette fonction est irréversible, souhaitez-vous continuer ?")
                user_choice = input("[oui, o | non, n]    -> ")
                yes_choices = ['oui', 'o']
                no_choices = ['non', 'n']

                if user_choice.lower() in yes_choices:
                    # Delete the archive
                    sql = f"""
                           DELETE FROM archives
                           WHERE identifiant_resident = "{identifiant_resident}";
                           """
                    #print(sql)

                    cursor.execute(sql)
                    db.commit()

                    print(f"\nL'archive '{identifiant_resident}' a bien été supprimée\n")

                    return True

                elif user_choice.lower() in no_choices:
                    print("\n")
                    return False

                else:
                    print("\n")
                    return False

            else:
                print("\nL'archive n'a pu être supprimée, car elle n'existe pas.\n")
                return False

        except Exception as e:
            print(f"Error 'del_an_archive' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    # Display Archives #
    @staticmethod
    def afficher_les_archives_console() -> bool:
        """Display the archive inside the terminal"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Fetch the archive
            sql = f""" SELECT * FROM archives; """
            cursor.execute(sql)
            result = cursor.fetchall()

            # Transform the result in dataframe and Display it
            result_df = pd.DataFrame(result, columns=['ID Résident', 'Date Entrée', 'Date Sortie'])
            result_df.index = result_df.index + 1    # Get start the count to 1 and no 0

            print("\n")
            print(result_df.to_markdown(tablefmt="grid"),"\n")

            return True

        except Exception as e:
            print(f"Error 'afficher_les_archives_console' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()


    @staticmethod
    def afficher_les_archives_streamlit() -> pd.DataFrame | bool:
        """Display Archive on streamlit"""

        try:
            db = mysqlco.connect(**CONFIG)
            cursor = db.cursor()

            # Fetch the archive
            sql = f""" SELECT * FROM archives; """
            cursor.execute(sql)
            result = cursor.fetchall()

            # Transform the result in dataframe and Display it
            result_df = pd.DataFrame(result, columns=['ID Résident', 'Date Entrée', 'Date Sortie'])
            result_df.index = result_df.index + 1    # Get start the count to 1 and no 0

            return result_df

        except Exception as e:
            print(f"Error 'afficher_les_archives_streamlit' : {e}")
            return False

        finally:
            if db.is_connected():
                db.close
                cursor.close()