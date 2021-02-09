# @Author: michael
# @Date:   01-Jan-1970
# @Filename: carto_conv_modif.py
# @Last modified by:   michael
# @Last modified time: 09-Feb-2021
# @License: GNU GPL v3


from datetime import datetime

import config as cfg
import telegram
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler)

from src.api.api_bdd import get_info
from src.api.button import build_menu
from src.plugins.carto.carto_tools import carto_creer_bouton_info
from src.plugins.carto.Ip import Ip

ETAPE1 = range(1)


def button_modif(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    context.user_data[0] = {0: id, 1: filtre}
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text="Quel Alias voulez vous donner ?",
                                  parse_mode=telegram.ParseMode.HTML)
    return ETAPE1


def etape1(update: Update, context: CallbackContext):
    query = update.callback_query
    message = update.message.text
    id = context.user_data[0][0]
    filtre = context.user_data[0][1]
    ip = Ip.get(Ip.id == id)
    ip.alias = message
    ip.save()
    reponse = "<b>L'alias a été mis à jour</b>\n\n"
    reponse += get_info(id, Table=Ip)
    reply_markup = carto_creer_bouton_info(id, filtre)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)
    return ConversationHandler.END


def conv_cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Bon c'est fini")
    return ConversationHandler.END
