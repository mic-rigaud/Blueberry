# @Author: michael
# @Date:   26-Sep-2019
# @Filename: nids-tools.py
# @Last modified by:   michael
# @Last modified time: 03-Apr-2020
# @License: GNU GPL v3


import json
import logging
from datetime import datetime, timedelta, timezone


class NidsTools():
    """Classe permettant de gerer Suricata. Caractérisé par:
    - log.
    """

    def __init__(self, log):
        self.log = log

    def get_last_log(self, intervalle):
        """Permet de recuperer les derniers logs."""
        try:
            offset_fr = timezone(timedelta(hours=2))
            date_last_veille = datetime.now(offset_fr) - timedelta(seconds=intervalle)
            logs_a_traiter = []
            with open(self.log, 'r') as file:
                for line in file:
                    line = line.replace('\0', '')
                    log = json.loads(line)
                    date = datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if date > date_last_veille:
                        logs_a_traiter.append(log)
            print(logs_a_traiter)
            return logs_a_traiter
        except PermissionError:
            logging.error("Permission Error")
            return "[ERROR] Vous n'avez pas les droits sur le fichier " + self.log
        except FileNotFoundError as exception:
            logging.error(exception)
            return "[ERROR] Fichier {} introuvable - il est possible que le fichier ne soit pas encore créé. Reessayez demain.".format(self.log)
        except Exception as exception:
            logging.warning(exception)
            return "[ERROR] Exception - " + str(exception)

    def get_rules(self):
        """Donne les regles appliqués."""
        pass
