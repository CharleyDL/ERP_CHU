#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 16 Dec. 2022
# ==============================================================================


import config
import modules.main_menu



#**** CONSTANTS ****#
MENU = modules.main_menu.erp()
CONFIG = config.get_db_config()


#**** MAIN ****#
if __name__ == '__main__':
    MENU