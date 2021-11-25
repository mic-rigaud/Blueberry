# @Author: michael
# @Date:   31-Dec-2019
# @Filename: carto.py
# @Last modified by:   michael
# @Last modified time: 11-Feb-2021
# @License: GNU GPL v3


"""Envoie une carto """

import logging
from datetime import datetime
from functools import partial
from subprocess import PIPE, Popen  # nosec

import config as cfg
import src.plugins.carto.carto_conv_modif as conv_modif
import telegram
from src.api.api_bdd import del_element, get_info, get_liste
from src.api.button import build_callback, build_menu
from src.api.button_bdd import button_modifier, button_supprimer
from src.api.Restricted import restricted
from src.api.send_alert import send_alert
from src.plugins.carto.carto_job import start_veille
from src.plugins.carto.carto_tools import (
    carto_creer_bouton_info,
    carto_ping,
    carto_ping_all,
    creer_carto,
    remplir_ip_voisin,
)
from src.plugins.carto.Ip import Ip
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
)

ORDERED = {
    "date": {0: Ip.time_first, 1: "croissant"},
    "dated": {0: Ip.time_first.desc(), 1: "descroissant"},
}
creer_bouton_liste = partial(
    get_liste, Table=Ip, plugins="carto", ordered_liste=ORDERED, ordered="dated"
)


def button_home(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = "Que souhaitez-vous faire?"
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_info(update: Update, context: CallbackContext):
    query = update.callback_query
    plugins = query.data.split("_")[0]
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    reponse = get_info(id, Table=Ip)
    reply_markup = carto_creer_bouton_info(id, filtre)
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_lister(update: Update, context: CallbackContext):
    query = update.callback_query
    reponse = "Voici la liste de vos cartos"
    filtre = query.data.split("_")
    if len(filtre) == 2:
        reponse = "Voici votre carto classé par date de rencontre {}\n".format(
            ORDERED["date"][1]
        )
        reply_markup = creer_bouton_liste()
    elif len(filtre) == 5:
        page = filtre[3]
        reponse = "Voici votre carto classé par date de rencontre {}".format(
            ORDERED[filtre[4]][1]
        )
        reply_markup = creer_bouton_liste(ordered=filtre[4], page=page)
    else:
        reponse = "Voici votre carto classé par date de rencontre {}".format(
            ORDERED[filtre[2]][1]
        )
        reply_markup = creer_bouton_liste(ordered=filtre[2])
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_graph(update: Update, context: CallbackContext):
    query = update.callback_query
    message = (
        "Attention cela peut prendre un certain temps\n\n"
        + "<i>Si le résultat attendu n'est pas satisfaisant c'est que soit:\n"
        + "- traceroute ne fait pas bien son travail. Ce qui arrive malheureusement... \n"
        + "- La base de donnée remplie par arpwatch est vide pour le moment."
        + " Vous pouvez forcer un scan manuel avec la commande /arpwatch</i>"
    )
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=message,
        parse_mode=telegram.ParseMode.HTML,
    )
    remplir_ip_voisin()
    creer_carto()
    context.bot.send_photo(
        chat_id=query.message.chat_id, photo=open("Network.gv.png", "rb")
    )


def button_ping(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    result = carto_ping(id)
    reponse = get_info(id, Table=Ip)
    reponse += "\n\n{}".format(result)
    reply_markup = carto_creer_bouton_info(id, filtre)
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_pingall(update: Update, context: CallbackContext):
    query = update.callback_query
    reponse = carto_ping_all()
    reply_markup = None
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_scan(update: Update, context: CallbackContext):
    query = update.callback_query
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    reponse = get_info(id, Table=Ip)
    reponse += "\n\nJe ne sais pas encore faire un Scan..."
    reply_markup = carto_creer_bouton_info(id, filtre)
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Graphique", callback_data="carto_graph"),
        InlineKeyboardButton("Lister", callback_data="carto_lister"),
        InlineKeyboardButton("Ping All", callback_data="carto_pingall"),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


@restricted
def carto(update: Update, context: CallbackContext):
    """Lance carto."""

    reponse = "Bienvenu dans votre outil de gestion de la carto\nQuel action souhaitez vous réaliser?"
    reply_markup = creer_bouton()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """Ajout la fonction carto."""
    dispatcher.add_handler(CommandHandler("carto", carto, pass_job_queue=True))
    dispatcher.add_handler(CallbackQueryHandler(button_info, pattern="carto_info."))
    dispatcher.add_handler(CallbackQueryHandler(button_ping, pattern="carto_ping_."))
    dispatcher.add_handler(
        CallbackQueryHandler(button_pingall, pattern="carto_pingall")
    )
    dispatcher.add_handler(CallbackQueryHandler(button_scan, pattern="carto_scan."))
    dispatcher.add_handler(CallbackQueryHandler(button_home, pattern="carto_home"))
    dispatcher.add_handler(CallbackQueryHandler(button_lister, pattern="^carto_liste."))
    dispatcher.add_handler(CallbackQueryHandler(button_graph, pattern="^carto_graph"))
    dispatcher.add_handler(CallbackQueryHandler(button_info, pattern="carto_info."))
    conv_carto = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(conv_modif.button_modif, pattern="^carto_modifier.")
        ],
        states={conv_modif.ETAPE1: [MessageHandler(Filters.text, conv_modif.etape1)]},
        fallbacks=[CommandHandler("end", conv_modif.conv_cancel)],
        conversation_timeout=120,
    )
    dispatcher.add_handler(conv_carto)
    start_veille(dispatcher.job_queue)
