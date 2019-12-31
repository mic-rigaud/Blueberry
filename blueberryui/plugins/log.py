# @Author: michael
# @Date:   11-Aug-2018
# @Filename: log.py
# @Last modified by:   michael
# @Last modified time: 31-Dec-2019
# @License: GNU GPL v3

"""Gere les logs."""

import logging

import telegram
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from api.Restricted import restricted

logFile = "log/blueberry.log"


def log_status():
    """Affiche les 10 dernieres lignes."""
    reponse = ""
    with open(logFile, "r") as file:
        for ligne in file.readlines()[-10:]:
            reponse += ligne.replace("<", "").replace("module",
                                                      "main").replace(">", "")
    return reponse


def log_rm():
    """Supprime les log."""
    with open(logFile, "w") as file:
        file.write("")
    logging.info("Fichier de log supprimé")


@restricted
def log(update: Update, context: CallbackContext):
    """Gere les log."""
    demande = ' '.join(context.args).lower().split(" ")[0]
    if demande == "ls" or demande == "":
        reponse = "<b>Voici les 10 derniers log:</b>\n"
        reponse += log_status()
    elif demande == "rm":
        reponse = "<b>Suppression des log.</b>"
        log_rm()
    else:
        reponse = "<b>Commande inexistante. Taper /help log</b>"
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """
    Gere les log.

    ls - affiche les 10 dernieres lignes
    rm - supprime les log
    """
    handler = CommandHandler('log', log, pass_args=True)
    dispatcher.add_handler(handler)
