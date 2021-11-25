# @Author: michael
# @Date:   01-Jan-1970
# @Filename: carto_job.py
# @Last modified by:   michael
# @Last modified time: 06-Feb-2021
# @License: GNU GPL v3


import logging
from datetime import time

from src.plugins.carto.carto_tools import carto_ping_all
from src.plugins.carto.Ip import Ip


def job_veille(context):
    """Affiche les alarmes."""
    carto_ping_all()


def start_veille(job_queue):
    """Lance la veille."""
    heures = 12
    datetime_heure = time(heures, 35)
    job_queue.run_daily(job_veille, datetime_heure, name="veille_carto")
    logging.info("Veille Topo lancé")
    return "Veille Lancé"
