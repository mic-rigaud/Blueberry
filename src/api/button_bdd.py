# @Author: michael
# @Date:   01-Jan-1970
# @Filename: button_bdd.py
# @Last modified by:   michael
# @Last modified time: 06-Feb-2021
# @License: GNU GPL v3
# @Author: michael
# @Date:   01-Jan-1970
# @Filename: telegram_button.py
# @Last modified by:   michael
# @Last modified time: 06-Feb-2021
# @License: GNU GPL v3


import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from src.api.api_bdd import del_element, get_info, get_info_more, get_liste
from src.api.button import build_menu
from src.plugins.carto.Ip import Ip

TABLES = {"carto": Ip}


def button_info(update: Update, context: CallbackContext):
    query = update.callback_query
    plugins = query.data.split("_")[0]
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    reponse = get_info(id, Table=TABLES[plugins])
    reply_markup = creer_bouton_info(plugins, id, filtre=filtre)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_moreinfo(update: Update, context: CallbackContext):
    query = update.callback_query
    plugins = query.data.split("_")[0]
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    reponse = get_info_more(id, Table=TABLES[plugins])
    reply_markup = creer_bouton_info(plugins, id, filtre=filtre)
    reponse_vierge = reponse.replace('<i>', '').replace(
        '</i>', '').replace('<b>', '').replace('</b>', '')
    if reponse_vierge == query.message.text:
        reponse += "~"
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def creer_bouton_info(plugins, id, filtre="nom"):
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("Modifier", callback_data="{}_modifier_{}".format(plugins, id)),
        InlineKeyboardButton(
            "Supprimer", callback_data="{}_suppr_{}_{}".format(plugins, id, filtre)),
        InlineKeyboardButton("Retour liste", callback_data="{}_lister_{}".format(plugins, filtre)),
        ]
    if plugins in ["sncf"]:
        button_list.append(InlineKeyboardButton("Plus d'info",
                                                callback_data="{}_moreinfo_{}_{}".format(plugins, id, filtre)))
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_supprimer(update: Update, context: CallbackContext):
    query = update.callback_query
    plugins = query.data.split("_")[0]
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    reponse = del_element(id, TABLES[plugins])
    button_list = [
        InlineKeyboardButton("Retour", callback_data="{}_lister_{}".format(plugins, filtre)),
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_modifier(update: Update, context: CallbackContext):
    query = update.callback_query
    plugins = query.data.split("_")[0]
    id = query.data.split("_")[2]
    filtre = query.data.split("_")[3]
    reponse = "<b>Fonction non implémenté</b>\n\n"
    reponse += get_info(id, Table=TABLES[plugins])
    reply_markup = creer_bouton_info(plugins, id, filtre=filtre)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_home(update: Update, context: CallbackContext):
    query = update.callback_query
    plugins = query.data.split("_")[0]
    mod = __import__("plugins." + plugins + '.' + plugins, fromlist=[''])
    reply_markup = mod.creer_bouton()
    reponse = "Que souhaitez-vous?"
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)
