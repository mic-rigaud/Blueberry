# @Author: michael
# @Date:   31-Mar-2020
# @Filename: arpwatch.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3


"""Affiche la base arpwatch et alerte lors d'une nouvelle entrée."""

import datetime
import logging

import config as cfg
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from src.api.button import build_menu
from src.api.Restricted import restricted
from src.api.send_alert import send_alert
from src.plugins.arpwatch.arpwatch_tools import arpwatch_liste, arpwatch_mqalert
from src.plugins.carto.Ip import Ip


def job_veille(context):
    """Affiche les alarmes."""
    arpwatch_mqalert(context)


def start_veille(job_queue):
    """Lance la veille."""
    heures = int(cfg.freq_arpwatch.split("h")[0])
    minutes = int(cfg.freq_arpwatch.split("h")[1])
    datetime_heure = datetime.time(heures, minutes)
    job_queue.run_daily(job_veille, datetime_heure, name="veille_arpwatch")
    logging.info("Veille lancé")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = "La veille n'est pas lancé.\n"
    job = job_queue.get_jobs_by_name("veille_arpwatch")
    for j in job:
        if not j.removed:
            reponse = (
                "La veille est lancé.\n"
                + "Un scan est réalisé tous les jours à "
                + cfg.freq_arpwatch
            )
    return reponse


###############################################################################


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton(
            "Rechercher une alerte manuellement", callback_data="arpwatch_alert"
        ),
        InlineKeyboardButton("Etat du job d'alerting", callback_data="arpwatch_job"),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_alert(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = None
    job_veille(context)
    reponse = "La recherche a été effectué avec succes."
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_job(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = get_info_veille(context.job_queue)
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


@restricted
def arpwatch(update: Update, context: CallbackContext):
    """Affiche la base arpwatch et alerte lors d'une nouvelle entrée."""
    reponse = arpwatch_liste()
    reply_markup = creer_bouton()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """
    Affiche la base arpwatch et alerte lors d'une nouvelle entrée.
    """
    dispatcher.add_handler(CommandHandler("arpwatch", arpwatch, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(button_job, pattern="^arpwatch_job$"))
    dispatcher.add_handler(
        CallbackQueryHandler(button_alert, pattern="^arpwatch_alert$")
    )
    start_veille(dispatcher.job_queue)
