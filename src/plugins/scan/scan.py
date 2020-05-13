# @Author: michael
# @Date:   10-May-2020
# @Filename: scan.py
# @Last modified by:   michael
# @Last modified time: 13-May-2020
# @License: GNU GPL v3

"""Scan une url/domain/ip/mail via les plugins dédiés."""


import re
import time

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from api.button import build_menu
from api.Restricted import restricted
from plugins.observatory.observatory import (get_http_observatory,
                                             get_tls_observatory)
from plugins.virustotal.virustotal import get_analyse_url, virus_scan_url
from plugins.whois.whois import get_whois


def creer_bouton(demande):
    """Creer la liste de boutons."""
    button_list = []
    re_ip = re.compile('[0-9]*\\.[0-9]*\\.[0-9]*\\.[0-9]*')
    if re_ip.match(demande):
        button_list.append(
            InlineKeyboardButton("Whois", callback_data="scan_wi_" + demande))
    elif '@' in demande:
        button_list.append(
            InlineKeyboardButton("Virustotal", callback_data="scan_vt_" + demande))
    else:
        button_list.append(
            InlineKeyboardButton("Analyse HTTP", callback_data="scan_ob_" + demande))
        button_list.append(
            InlineKeyboardButton("Virustotal", callback_data="scan_vt_" + demande))
        button_list.append(
            InlineKeyboardButton("Whois", callback_data="scan_wi_" + demande))
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_action(update: Update, context: CallbackContext):
    query = update.callback_query
    url = query.data.split("_")[2]
    action = query.data.split("_")[1]
    if action == "wi":
        reponse = get_whois(url)
    elif action == "ob":
        reponse = get_http_observatory(url)
        if url in reponse:
            reponse += get_tls_observatory(url)
    elif action == "vt":
        id_virus = virus_scan_url(url)
        time.sleep(5)
        reponse = get_analyse_url(id_virus)
    else:
        reponse = "Pardon je n'ai pas compris la demande"
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML)
    reply_markup = creer_bouton(url)
    reponse = "Souhaitez vous lancer une autre analyse?"
    context.bot.send_message(chat_id=query.message.chat_id,
                             text=reponse,
                             reply_markup=reply_markup)


@restricted
def scan(update: Update, context: CallbackContext):
    """Affiche le status de la raspberry."""
    demande = ' '.join(context.args).lower().split(" ")[0]
    reply_markup = None
    if demande != "":
        reponse = "Quel analyse souhaitez-vous lancer?"
        reply_markup = creer_bouton(demande)
    else:
        reponse = "Faire \"/scan <i>url/domain/ip/mail</i>\""

    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)


def add(dispatcher):
    """
    Scan une url/domain/ip/mail via les plugins dédiés.
    """
    dispatcher.add_handler(CommandHandler('scan', scan))
    dispatcher.add_handler(CallbackQueryHandler(button_action, pattern="scan_wi_."))
    dispatcher.add_handler(CallbackQueryHandler(button_action, pattern="scan_ob_."))
    dispatcher.add_handler(CallbackQueryHandler(button_action, pattern="scan_vt_."))
