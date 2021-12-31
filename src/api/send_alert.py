# @Author: michael
# @Date:   02-Apr-2020
# @Filename: send_alert.py
# @Last modified by:   michael
# @Last modified time: 02-Apr-2020
# @License: GNU GPL v3

import config as cfg
import telegram


def send_alert(context, message, reply_markup=None):
    for chat_id in cfg.user:
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup,
        )
