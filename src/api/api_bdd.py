# @Author: michael
# @Date:   28-Oct-2017
# @Project: Blueberry
# @Filename: api_bdd.py
# @Last modified by:   michael
# @Last modified time: 06-Feb-2021
# @License: GNU GPL v3

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler)

from src.api.button import build_menu

NUMBER_LISTE = 15


def get_liste(Table, plugins, ordered_liste, ordered, exp=True):
    try:
        if ordered[-1] == "d":
            filtre_d = ordered[:-1]
        else:
            filtre_d = ordered + "d"
        button_list = []
        for element in Table.select().where(exp).order_by(ordered_liste[ordered][0]).limit(NUMBER_LISTE):
            line = element.str_compact()
            if line:
                button_list.append(InlineKeyboardButton(
                    line, callback_data="{}_info_{}_{}".format(plugins, element.id, ordered)))
        button_list.append(InlineKeyboardButton(
            "Ordre descroissant", callback_data="{}_lister_{}".format(plugins, filtre_d)))
        button_list.append(InlineKeyboardButton("Retour", callback_data="{}_home".format(plugins)))
        return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    except Exception as e:
        logging.warning("Aucun élément dans la liste\n" + str(e))


def get_info(id, Table):
    try:
        element_selected = Table.get(Table.id == id)
        return element_selected.__str__()
    except Exception as e:
        logging.warning(e)


def get_info_more(id, Table):
    try:
        element_selected = Table.get(Table.id == id)
        return element_selected.__str__() + "\n\n" + element_selected.more_info()
    except Exception as e:
        logging.warning(e)


def del_element(id, Table):
    try:
        Table.delete().where(Table.id == id).execute()
        return "Suppression avec succes"
    except Exception as e:
        logging.warning(e)
