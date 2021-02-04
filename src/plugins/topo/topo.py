# @Author: michael
# @Date:   31-Dec-2019
# @Filename: topo.py
# @Last modified by:   michael
# @Last modified time: 04-Feb-2021
# @License: GNU GPL v3


"""Envoie une topo """

import logging
from datetime import datetime
from subprocess import PIPE, Popen  # nosec

import config as cfg
import telegram
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from src.api.api_bdd import Ip, get_info
from src.api.network import ping
from src.api.Restricted import restricted
from src.plugins.topo.topo_tools import creer_button_info, creer_button_ip


def button_info(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query.data.split("_")[2]
    reponse = get_info(id, Table=Ip)
    reply_markup = creer_button_info(id)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_ping(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query.data.split("_")[2]
    ip = Ip.get(Ip.id == id)
    if ping(ip.ip) == 0:
        result = "La machine est en ligne"
        ip.isonline()
        ip.save()
    else:
        result = "La machine est hors ligne"
    reponse = get_info(id, Table=Ip)
    reponse += "\n\n{}".format(result)
    reply_markup = None
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_scan(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query.data.split("_")[2]
    reponse = get_info(id, Table=Ip)
    reply_markup = None
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


@restricted
def topo(update: Update, context: CallbackContext):
    """Lance topo."""
    message = "test en cours"
    reply_markup = creer_button_ip()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=message,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)


def add(dispatcher):
    """Ajout la fonction topo."""
    dispatcher.add_handler(CommandHandler('topo', topo, pass_job_queue=True))
    dispatcher.add_handler(CallbackQueryHandler(button_info, pattern="topo_info."))
    dispatcher.add_handler(CallbackQueryHandler(button_ping, pattern="topo_ping."))
    dispatcher.add_handler(CallbackQueryHandler(button_scan, pattern="topo_scan."))
