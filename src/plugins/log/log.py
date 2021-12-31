# @Author: michael
# @Date:   11-Aug-2018
# @Filename: log.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3

"""Gere les logs."""

import logging

import config as cfg
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from src.api.button import build_menu
from src.api.Restricted import restricted


def log_liste():
    """Affiche les 10 dernieres lignes."""
    reponse = "<b>Voici les 10 derniers log:</b>\n"
    with open(cfg.log, "r") as file:
        for ligne in file.readlines()[-10:]:
            reponse += ligne.replace("<", "").replace("module", "main").replace(">", "")
    return reponse


def log_rm():
    """Supprime les log."""
    with open(cfg.log, "w") as file:
        file.write("")
    logging.info("Fichier de log supprimé")
    return "<b>Suppression des logs effectuée.</b>"


###############################################################################
def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("liste", callback_data="log_liste"),
        InlineKeyboardButton("supprimer", callback_data="log_supprimer"),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = log_liste()
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def button_supprimer(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = log_rm()
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


@restricted
def log(update: Update, context: CallbackContext):
    """Gere les log."""
    reponse = log_liste()
    reply_markup = creer_bouton()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """
    Gere les log.

    ls - affiche les 10 dernieres lignes
    rm - supprime les log
    """
    dispatcher.add_handler(CommandHandler("log", log, pass_args=True))
    dispatcher.add_handler(
        CallbackQueryHandler(button_supprimer, pattern="^log_supprimer$")
    )
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^log_liste$"))
