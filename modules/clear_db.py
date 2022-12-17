#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import mysql.connector as mysqlco

from mysql.connector import Error

import config


#**** CONSTANTS ****#
CONFIG = config.get_db_config()




def clear_patient_table() -> bool:
    """Delete definitively the Patient table"""

    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        sql = f"""TRUNCATE TABLE patients;"""
        cursor.execute(sql)

        return True

    except Exception as e:
        print(f"Error 'clear_patient_table' : {e}")
        return False

    finally:
        if db.is_connected():
            db.close
            cursor.close()


def clear_employee_table() -> bool:
    """Delete definitively the HR table"""

    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        sql = f"""TRUNCATE TABLE rh;"""
        cursor.execute(sql)

        return True

    except Exception as e:
        print(f"Error 'clear_employee_table' : {e}")
        return False

    finally:
        if db.is_connected():
            db.close
            cursor.close()


def clear_archive_table() -> bool:
    """Delete definitively the Archive table"""

    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        sql = f"""TRUNCATE TABLE archives;"""
        cursor.execute(sql)

        return True

    except Exception as e:
        print(f"Error 'clear_archive_table' : {e}")
        return False

    finally:
        if db.is_connected():
            db.close
            cursor.close()


def clear_all() -> bool:
    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        sql = f"""
                TRUNCATE TABLE patients;
                TRUNCATE TABLE rh;
                TRUNCATE TABLE archives;
               """
        cursor.execute(sql)

        return True

    except Exception as e:
        print(f"Error 'clear_all' : {e}")
        return False

    finally:
        if db.is_connected():
            db.close
            cursor.close()