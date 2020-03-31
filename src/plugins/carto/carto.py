# @Author: michael
# @Date:   31-Dec-2019
# @Filename: carto.py
# @Last modified by:   michael
# @Last modified time: 31-Dec-2019
# @License: GNU GPL v3


"""Envoie une carto """

from datetime import datetime

import config as cfg
import telegram
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from api.api_bdd import Ip
from api.Restricted import restricted


def job_veille(context):
    """Affiche les alarmes."""
    message = ""
    for ip in Ip.select():
        time_last = ip.time_last
        if ip.status:
            status = "✅"
        else:
            status = "☠️"
        message += "{} {}@{} - last: {}\n".format(status, ip.host, ip.ip, time_last)
    context.bot.send_message(chat_id=245779512,
                             text=message)


def start_veille(job_queue):
    """Lance la veille."""
    job_queue.run_repeating(job_veille,
                            cfg.freq_carto,
                            first=datetime.now(),
                            name="veille_carto")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = ""
    job = job_queue.get_jobs_by_name("veille_carto")
    for j in job:
        if not j.removed:
            reponse += "La veille est lancé.\n"
    return reponse


@restricted
def carto(update: Update, context: CallbackContext):
    """Lance carto."""
    message = get_info_veille(context.job_queue)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=message, parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """Ajout la fonction carto."""
    handler = CommandHandler('carto', carto,
                             pass_job_queue=True)
    dispatcher.add_handler(handler)
    start_veille(dispatcher.job_queue)
