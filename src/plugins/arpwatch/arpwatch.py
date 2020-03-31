# @Author: michael
# @Date:   31-Mar-2020
# @Filename: arpwatch.py
# @Last modified by:   michael
# @Last modified time: 31-Mar-2020
# @License: GNU GPL v3


"""Affiche la base arpwatch et alerte lors d'une nouvelle entrée."""

import datetime
import logging

import config as cfg
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from api.button import build_menu
from api.Restricted import restricted


def job_veille(context):
    """Affiche les alarmes."""
    logs = arpwatch_liste()
    context.bot.send_message(chat_id=245779512,
                             text=logs)


def start_veille(job_queue):
    """Lance la veille."""
    heure = datetime.time(7, 00)
    job_queue.run_daily(job_veille,
                        heure,
                        name="veille_arpwatch")
    logging.info("Veille lancé")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = "La veille n'est pas lancé.\n"
    job = job_queue.get_jobs_by_name("veille_arpwatch")
    for j in job:
        if not j.removed:
            reponse = "La veille est lancé.\n"
    return reponse


def arpwatch_liste():
    try:
        reponse = ""
        with open(cfg.arpwatch_mail, 'r') as file:
            contenu = parse(file.readlines())
            for id in contenu:
                element = contenu[id]
                reponse += "{}  {}  {}\n".format(element["hostname"], element["ip"],
                                                 element["timestamp"])
            reponse = reponse.replace("<", "").replace(">", "")
            return reponse
    except Exception as exception:
        logging.warning(exception)
        return "Probleme avec les logs"


def parse(lines):
    retour = {}
    i = -1
    for line in lines:
        if line == "---\n":
            i += 1
            retour[i] = {"hostname": "",
                         "ip": "",
                         "vendor": "",
                         "timestamp": "",
                         "mac": ""}
        elif "hostname" in line:
            retour[i]["hostname"] = line.split(': ')[1].replace('\n', '')
        elif "ip address" in line:
            retour[i]["ip"] = line.split(': ')[1].replace('\n', '')
        elif "ethernet vendor" in line:
            retour[i]["vendor"] = line.split(': ')[1].replace('\n', '')
        elif "timestamp" in line:
            retour[i]["timestamp"] = line.split(': ')[1].replace('\n', '')
        elif "ethernet address" in line:
            retour[i]["mac"] = line.split(': ')[1].replace('\n', '')
    return retour

###############################################################################


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("afficher", callback_data="arpwatch_liste"),
        InlineKeyboardButton("etat job", callback_data="arpwatch_job"),
        ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = arpwatch_liste()
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_job(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = "Ne fonctionne pas pour le moment"  # get_info_veille(context.job_queue)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


@restricted
def arpwatch(update: Update, context: CallbackContext):
    """Affiche la base arpwatch et alerte lors d'une nouvelle entrée."""
    reponse = "Que puis-je faire pour vous?"
    reply_markup = creer_bouton()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)


def add(dispatcher):
    """
    Affiche la base arpwatch et alerte lors d'une nouvelle entrée.
    """
    dispatcher.add_handler(CommandHandler('arpwatch', arpwatch, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(button_job, pattern="^arpwatch_job$"))
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^arpwatch_liste$"))
    # start_veille(dispatcher.job_queue)
