# @Author: michael
# @Date:   13-Feb-2018
# @Project: Blueberry
# @Filename: main.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3


import logging
import os
import sys
from multiprocessing import Process

import config as cfg
import telegram
from telegram import Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Filters, MessageHandler, Updater)

from src.api.button import button
from src.api.mq_pull import mqPull
from src.api.Restricted import restricted

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

logging.basicConfig(
    filename=cfg.log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

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
        nom = mod.__name__.replace("src.plugins.", "").split('.')[0]
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
    lst_import = os.listdir("./src/plugins")
    for module_name in lst_import:
        if "_" not in module_name:
            mod = __import__("src.plugins." + module_name + '.' + module_name, fromlist=[''])
            mod.add(dispatcher)
            HELP_LIST.append(mod)
    help_handler = CommandHandler('help', help, pass_args=True)
    dispatcher.add_handler(help_handler)
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)


if __name__ == "__main__":
    logging.info("Demarrage de Blueberry")

    updater = Updater(token=cfg.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    charge_plugins(dispatcher)
    mq_pull = Process(target=mqPull, args=(updater,))
    mq_pull.start()
    updater.start_polling()
    updater.idle()
    mq_pull.terminate()
    logging.info("Extinction de Blueberry")
