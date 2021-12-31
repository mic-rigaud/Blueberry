# @Author: michael
# @Date:   09-Feb-2018
# @Project: Major_Home
# @Filename: nids.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3

"""Envoie les alarmes NIDS"""

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from src.api.Restricted import restricted
from src.api.button import build_menu
from src.plugins.nids.nids_tools import start_veille, get_info_veille, nids_alert


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Dernières alertes", callback_data="nids_test"),
        InlineKeyboardButton("Etat job", callback_data="nids_job"),
        InlineKeyboardButton("Règles Suricata", callback_data="nids_rules"),
    ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_alert(update: Update, context: CallbackContext):
    query = update.callback_query
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Recherche en cours.\n<i>Attention cela peut mettre un certain temps.</i>",
        parse_mode=telegram.ParseMode.HTML,
    )
    messages = nids_alert(all=True)
    for message in messages:
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode=telegram.ParseMode.HTML,
        )
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Recherche terminé.",
        parse_mode=telegram.ParseMode.HTML,
    )


def button_job(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = get_info_veille(context.job_queue)
    context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=reponse,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


@restricted
def nids(update: Update, context: CallbackContext):
    """Lance nids."""
    message = "Que puis-je faire pour vous?"
    reply_markup = creer_bouton()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=message,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """Ajout la fonction nids."""
    dispatcher.add_handler(CommandHandler("nids", nids, pass_job_queue=True))
    dispatcher.add_handler(CallbackQueryHandler(button_job, pattern="^nids_job$"))
    dispatcher.add_handler(CallbackQueryHandler(button_alert, pattern="^nids_test$"))
    start_veille(dispatcher.job_queue)
