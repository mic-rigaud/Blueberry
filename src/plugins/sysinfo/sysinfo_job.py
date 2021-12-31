import logging
from datetime import time

from src.api.send_alert import send_alert
from src.plugins.sysinfo.sysinfo_tool import sysinfo_job


def job_veille(context):
    """Affiche les alarmes."""
    reponse = sysinfo_job()
    if reponse != "":
        send_alert(context, reponse)


def start_veille(job_queue):
    """Lance la veille."""
    job_queue.run_repeating(job_veille, 360, first=5, name="veille_sysinfo")
    logging.info("Veille Sysinfo lancé")
    return "Veille Lancé"
