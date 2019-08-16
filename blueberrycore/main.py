# @Author: michael
# @Date:   02-Jul-2019
# @Filename: main.py
# @Last modified by:   michael
# @Last modified time: 16-Aug-2019
# @License: GNU GPL v3

import logging
import os
import sys
import time

import config as cfg
import schedule

# Creating a function which will print hello world
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

logging.basicConfig(
    filename=cfg.log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')


def charge_plugins():
    """Charge l'ensemble des plugins."""
    lst_import = os.listdir(cfg.dir + "blueberrycore/plugins")
    for module in lst_import:
        if ".py" in module:
            module_name = module.split(".py")[0]
            mod = __import__("plugins." + module_name, fromlist=[''])
            mod.add()


if __name__ == "__main__":
    # TODO: Verifier qu'on a les droits roots
    charge_plugins()
    while True:
        schedule.run_pending()
        time.sleep(2)
        # TODO: Prévoir le moyen de kill
