# @Author: michael
# @Date:   11-Jan-2020
# @Filename: sysinfo.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3


"""Affiche le status de la raspberry."""

import psutil
import telegram
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from src.api.Restricted import restricted
from src.plugins.sysinfo.sysinfo_job import start_veille
from src.plugins.sysinfo.sysinfo_tool import status_str


@restricted
def sysinfo(update: Update, context: CallbackContext):
    """Affiche le status de la raspberry."""
    reponse = status_str()
    context.bot.send_message(
        chat_id=update.message.chat_id, text=reponse, parse_mode=telegram.ParseMode.HTML
    )


def add(dispatcher):
    """
    Affiche le status de la raspberry.
    """
    handler = CommandHandler("sysinfo", sysinfo)
    dispatcher.add_handler(handler)
    start_veille(dispatcher.job_queue)
