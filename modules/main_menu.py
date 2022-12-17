#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import sys
import webbrowser

from os import system
import streamlit.web.cli as stcli

import modules.console_navigation as cn




def header() -> None:
    """Display the 'CHU ERP' HEADER"""

    with open('./img/header.txt', 'r') as f:
        print(f.read())


def choice() -> int:
    """Get the user's choice"""

    try:
        choice = int(input("\nVotre choix : "))

    except Exception as e:
        print(e)

    return choice


def web_app() -> None:
    """Display the link to open the webapp"""

    system('clear')    # Clear the terminal

    # Display the header
    header()
    print("   -- Cliquer sur le URL NETWORK pour accéder à la Web App :")

    # Launch the streamlit app with the terminal cmd 'run'
    sys.argv = ["streamlit", "run", "streamlit_app.py"]
    sys.exit(stcli.main())


def main_menu() -> int:
    """Display the main menu : continue with terminal or webapp"""

    system('clear')    # Clear the terminal

    # Display the header and options
    header()
    print("   -- 1 : Gérer via le Terminal")
    print("   -- 2 : Gérer via la Web App")
    print("   -- 3 : Quitter")

    # Get the user choice
    menu_choice = choice()

    return menu_choice


def erp() -> None:
    """Initiate the ERP menu"""

    while True:
        #**** MAIN MENU : choosing between terminal or web app ****#
        navigation_choice = main_menu()

        #**** TERMINAL NAVIGATION ****#
        if navigation_choice == 1:
            cn.console_erp()

        #**** WEB APP NAVIGATION ****#
        elif navigation_choice == 2:
            # Renvoie sur la page web
            web_app()

        #**** END PROGRAM ****#
        else:
            sys.exit()