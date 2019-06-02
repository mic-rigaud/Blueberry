# @Author: michael
# @Date:   13-Feb-2018
# @Project: Blueberry
# @Filename: main.py
# @Last modified by:   michael
# @Last modified time: 02-Jun-2019
# @License: GNU GPL v3


import logging
import os
import sys

import config as cfg
import telegram
from api.button import button
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

logging.basicConfig(
    filename=cfg.log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

help_list = []


def unknown(bot, update):
    """Gere la reponse pour une commande inconnue."""
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Commande inconnue")


def help(bot, update, args):
    """Affiche l'aide."""
    demande = ' '.join(args).lower().split(" ")[0]
    reponse = "Blueberry possède les plugins suivants:\n\n"
    for mod in help_list:
        doc = mod.__doc__
        nom = mod.__name__.replace("plugins.", "")
        if doc:
            if demande == "":
                reponse += "<b>" + nom + "</b> : " + doc + "\n"
            elif demande in nom:
                reponse = mod.add.__doc__
    bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML)


def charge_plugins(dispatcher):
    """Charge l'ensemble des plugins."""
    lst_import = os.listdir("./blueberry/plugins")
    for module in lst_import:
        if ".py" in module:
            module_name = module.split(".py")[0]
            mod = __import__("plugins." + module_name, fromlist=[''])
            mod.add(dispatcher)
            help_list.append(mod)
    help_handler = CommandHandler('help', help, pass_args=True)
    dispatcher.add_handler(help_handler)
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(CallbackQueryHandler(button, pass_job_queue=True))


if __name__ == "__main__":
    logging.info("Demarrage de Blueberry")

    updater = Updater(token=cfg.bot_token)
    dispatcher = updater.dispatcher
    charge_plugins(dispatcher)
    updater.start_polling()
    updater.idle()

    logging.info("Extinction de Blueberry")
