#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================
# Configuration file for the connection to DB
# ==============================================================================


def get_db_config() -> dict:
    """
    Returns a dictionary containing database's informations, which are used
    by the following method : mysql.connector.connect()
    """

    config = {
            "host" : "localhost",
            "user" : "root",
            "password" : "example",
            "auth_plugin" : "mysql_native_password",
            "port" : "3307",
            "database" : "CHU_Caen"
    }

    return config