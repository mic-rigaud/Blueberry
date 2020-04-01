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
    messages = nids_alert()
    if "Il n'y a pas" not in messages[0]:
        for message in messages:
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


def nids_alert():
    message = []
    evenements = NidsTools(cfg.suricata_log).get_last_log(cfg.freq_nids)
    if evenements == []:
        return ["Il n'y a pas d'évènements"]
    if evenements == "PermissionError" or evenements == "Exception" or evenements == "Fichier introuvable":
        return ["Il y a le problème suivant: " + str(evenements)]
    for event in evenements:
        if event["event_type"] == "alert":
            message_test = str(event).replace(' ', '').replace('\n', '')
            if message_test != "":
                message.append(message_test)
    if message == []:
        return ["Il n'y a pas d'alertes"]
    return message

###############################################################################


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Dernières alertes", callback_data="nids_test"),
        InlineKeyboardButton("Etat job", callback_data="nids_job"),
        ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_alert(update: Update, context: CallbackContext):
    query = update.callback_query
    messages = nids_alert()
    for message in messages:
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text=message,
                                 parse_mode=telegram.ParseMode.HTML)


def button_job(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = get_info_veille(context.job_queue)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


@restricted
def nids(update: Update, context: CallbackContext):
    """Lance nids."""
    message = "Que puis-je faire pour vous?"
    reply_markup = creer_bouton()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=message,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)


def add(dispatcher):
    """Ajout la fonction nids."""
    dispatcher.add_handler(CommandHandler('nids', nids, pass_job_queue=True))
    dispatcher.add_handler(CallbackQueryHandler(button_job, pattern="^nids_job$"))
    dispatcher.add_handler(CallbackQueryHandler(button_alert, pattern="^nids_test$"))
    start_veille(dispatcher.job_queue)
