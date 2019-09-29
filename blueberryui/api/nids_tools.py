# @Author: michael
# @Date:   26-Sep-2019
# @Filename: nids-tools.py
# @Last modified by:   michael
# @Last modified time: 29-Sep-2019
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
        offset = timezone(timedelta(hours=2))
        date_last_veille = datetime.now(offset) - timedelta(seconds=intervalle)
        logs_a_traiter = []
        with open(self.log, 'r+') as file:
            for line in file:
                try:
                    log = json.loads(line)
                    date = datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if date > date_last_veille:
                        logs_a_traiter.append(log)
                except Exception as exception:
                    logging.info(exception)
        return logs_a_traiter

    def get_rules(self):
        """Donne les regles appliqués."""
        pass
