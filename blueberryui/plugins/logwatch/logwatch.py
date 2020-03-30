# @Author: michael
# @Date:   30-Mar-2020
# @Filename: watchlog.py
# @Last modified by:   michael
# @Last modified time: 30-Mar-2020
# @License: GNU GPL v3

"""Affiche les logs en utilisant logwatch."""

import datetime
import logging

import config as cfg
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from api.button import build_menu
from api.Restricted import restricted

REPORT = "/var/cache/logwatch/report"
#REPORT = "./report-test"


def job_veille(context):
    """Affiche les alarmes."""
    logs = logwatch_liste()
    context.bot.send_message(chat_id=245779512,
                             text=logs)


def start_veille(job_queue):
    """Lance la veille."""
    heure = datetime.time(7, 00)
    job_queue.run_daily(job_veille,
                        heure,
                        name="veille_logwatch")
    logging.info("Veille lancé")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = "La veille n'est pas lancé.\n"
    job = job_queue.get_jobs_by_name("veille_logwatch")
    for j in job:
        if not j.removed:
            reponse = "La veille est lancé.\n"
    return reponse


def logwatch_liste():
    try:
        reponse = ""
        with open(REPORT, 'r') as file:
            for line in file:
                if line != "\n" and line != " \n":
                    if "End" in line:
                        reponse += "\n"
                    else:
                        reponse += line
        if reponse == "" or reponse == "\n":
            return "Pas de log pour le moment"
        reponse = reponse.replace("###", "#")
        return reponse
    except:
        return "Probleme avec les logs"

###############################################################################


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("afficher", callback_data="logwatch_liste"),
        InlineKeyboardButton("etat job", callback_data="logwatch_job"),
        ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = logwatch_liste()
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


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
def logwatch(update: Update, context: CallbackContext):
    """Gere les log."""
    reponse = "Que puis-je faire pour vous?"
    reply_markup = creer_bouton()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)


def add(dispatcher):
    """
    Gere les log.

    ls - affiche les 10 dernieres lignes
    rm - supprime les log
    """
    dispatcher.add_handler(CommandHandler('logwatch', logwatch, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(button_job, pattern="^logwatch_job$"))
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^logwatch_liste$"))
    start_veille(dispatcher.job_queue)
