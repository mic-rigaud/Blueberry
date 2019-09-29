# @Author: michael
# @Date:   09-Feb-2018
# @Project: Major_Home
# @Filename: nids.py
# @Last modified by:   michael
# @Last modified time: 29-Sep-2019
# @License: GNU GPL v3

"""Envoie les alarmes NIDS"""

import telegram
from telegram.ext import CommandHandler

from api.nids_tools import NidsTools
from api.Restricted import restricted

LOG = "/var/log/suricata/eve.json"
#LOG = "./blueberryui/tests/data/suricata-log.json"

INTERVALLE = 3600


def job_veille(bot, job):
    """Affiche les alarmes."""
    logs = NidsTools(LOG).get_last_log(INTERVALLE)
    if logs != {}:
        for log in logs:
            if log["event_type"] == "alert":
                message = str(log)
                bot.send_message(chat_id=245779512,
                                 text=message)


def start_veille(job_queue):
    """Lance la veille."""
    job_queue.run_repeating(job_veille,
                            INTERVALLE,
                            name="veille_nids")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = ""
    job = job_queue.get_jobs_by_name("veille_nids")
    for j in job:
        if not j.removed:
            reponse += "La veille est lancé.\n"
    return reponse


@restricted
def nids(bot, update, job_queue):
    """Lance nids."""
    message = get_info_veille(job_queue)
    bot.send_message(chat_id=update.message.chat_id,
                     text=message, parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """Ajout la fonction nids."""
    handler = CommandHandler('nids', nids,
                             pass_job_queue=True)
    dispatcher.add_handler(handler)
    start_veille(dispatcher.job_queue)
