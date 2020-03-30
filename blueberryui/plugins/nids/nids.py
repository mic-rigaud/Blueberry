# @Author: michael
# @Date:   09-Feb-2018
# @Project: Major_Home
# @Filename: nids.py
# @Last modified by:   michael
# @Last modified time: 31-Dec-2019
# @License: GNU GPL v3

"""Envoie les alarmes NIDS"""

import logging
from datetime import datetime

import config as cfg
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from api.button import build_menu
from api.Restricted import restricted
from plugins.nids.nids_tools import NidsTools


def job_veille(context):
    """Affiche les alarmes."""
    logs = NidsTools(cfg.suricata_log).get_last_log(cfg.freq_nids)
    if logs == "PermissionError" or logs == "Exception":
        context.bot.send_message(chat_id=245779512,
                                 text=logs)
    elif logs != {}:
        for log in logs:
            if log["event_type"] == "alert":
                message = str(log)
                if message != "":
                    context.bot.send_message(chat_id=245779512,
                                             text=message)


def start_veille(job_queue):
    """Lance la veille."""
    job_queue.run_repeating(job_veille,
                            cfg.freq_nids,
                            first=datetime.now(),
                            name="veille_nids")
    logging.info("Veille lancé")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = "La veille n'est pas lancé.\n"
    job = job_queue.get_jobs_by_name("veille_nids")
    for j in job:
        if not j.removed:
            reponse = "La veille est lancé.\n"
    return reponse

###############################################################################

#
# def creer_bouton():
#     """Creer la liste de boutons."""
#     button_list = [
#         InlineKeyboardButton("liste", callback_data="log_liste"),
#         InlineKeyboardButton("supprimer", callback_data="log_supprimer"),
#         ]
#     return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


@restricted
def nids(update: Update, context: CallbackContext):
    """Lance nids."""
    message = get_info_veille(context.job_queue)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=message, parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """Ajout la fonction nids."""
    dispatcher.add_handler(CommandHandler('nids', nids, pass_job_queue=True))
    start_veille(dispatcher.job_queue)
