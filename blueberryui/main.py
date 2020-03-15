# @Author: michael
# @Date:   13-Feb-2018
# @Project: Blueberry
# @Filename: main.py
# @Last modified by:   michael
# @Last modified time: 31-Dec-2019
# @License: GNU GPL v3


import logging
import os
import sys

import config as cfg
import telegram
from telegram import Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, MessageHandler, Updater)

from api.button import button
from api.Restricted import restricted

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

logging.basicConfig(
    filename=cfg.log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

HELP_LIST = []


@restricted
def unknown(update: Update, context: CallbackContext):
    """Gere la reponse pour une commande inconnue."""
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Commande inconnue")


@restricted
def help(update: Update, context: CallbackContext):
    """Affiche l'aide."""
    demande = ' '.join(context.args).lower().split(" ")[0]
    reponse = "Blueberry possède les plugins suivants:\n\n"
    for mod in HELP_LIST:
        doc = mod.__doc__
        nom = mod.__name__.replace("plugins.", "")
        if doc:
            if demande == "":
                reponse += "<b>" + nom + "</b> : " + doc + "\n"
            elif demande in nom:
                reponse = mod.add.__doc__
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML)


def charge_plugins(dispatcher):
    """Charge l'ensemble des plugins."""
    lst_import = os.listdir("./blueberryui/plugins")
    for module_name in lst_import:
        mod = __import__("plugins." + module_name, fromlist=[''])
        mod.add(dispatcher)
        HELP_LIST.append(mod)
    help_handler = CommandHandler('help', help, pass_args=True)
    dispatcher.add_handler(help_handler)
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(CallbackQueryHandler(button, pass_job_queue=True))


if __name__ == "__main__":
    logging.info("Demarrage de Blueberry")

    updater = Updater(token=cfg.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    charge_plugins(dispatcher)
    updater.start_polling()
    updater.idle()

    logging.info("Extinction de Blueberry")
