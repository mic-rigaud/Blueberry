# @Author: michael
# @Date:   27-Apr-2019
# @Filename: button.py
# @Last modified by:   michael
# @Last modified time: 28-Apr-2019
# @License: GNU GPL v3
import json

import telegram
from api.Restricted import restricted


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    """Permet de construire un menu interactif."""
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


@restricted
def button(bot, update, job_queue):
    query = update.callback_query
    try:
        data = json.loads(query.data)
    except json.JSONDecodeError:
        data = query.data

    module_name = data["module"]
    mod = __import__("actions." + module_name, fromlist=[''])
    reponse, reply_markup = mod.button(bot, update, job_queue)

    bot.edit_message_text(
        text=reponse,
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=reply_markup)


def build_callback(data):
    return_value = json.dumps(data)
    if len(return_value) > 64:
        raise TelegramCallbackError(
            "Les data ont une taille supérieur à 64 bytes")
    return return_value


class TelegramCallbackError(Exception):
    def __init__(self, message=""):
        self.message = message
