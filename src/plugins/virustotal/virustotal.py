# @Author: michael
# @Date:   23-Apr-2020
# @Filename: virustotal.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3


"""Analyse une url avec virustotal."""

import json
import logging
import time

import config as cfg
import psutil
import requests
import telegram
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from src.api.Restricted import restricted

ADRESSE = "https://www.virustotal.com/api/v3/urls"
HEADERS = {"x-apikey": cfg.virustotal_key}


def print_analyse(analyse):
    try:
        reponse = "<b>Voici l'analyse pour {}:</b>\n".format(
            analyse["data"]["attributes"]["last_final_url"])
        for scanner in analyse["data"]["attributes"]["last_analysis_results"]:
            result = analyse["data"]["attributes"]["last_analysis_results"][scanner]["result"]
            if result == "clean":
                result_icon = "✅"
            elif result == "unrated":
                result_icon = "❓"
            else:
                result_icon = "❌"
            reponse += "{} - {}\n".format(result_icon, scanner)
        return reponse
    except KeyError:
        logging.error("Analyse retournée par virustotal erronée")
        return "[ERROR] analyse fourni par virustotal inexploitable"


def virus_scan_url(url):
    data = {"url": url}
    session = requests.Session()
    req = session.post(ADRESSE, headers=HEADERS, data=data)
    reponse = json.loads(req.content.decode("utf-8"))
    return reponse["data"]["id"].split('-')[1]


def get_analyse_url(id_suspect):
    req = requests.get(ADRESSE + "/" + id_suspect, headers=HEADERS)
    analyse = json.loads(req.content.decode("utf-8"))
    return print_analyse(analyse)


@restricted
def virustotal(update: Update, context: CallbackContext):
    """Affiche le status de la raspberry."""
    demande = ' '.join(context.args).lower().split(" ")[0]
    reponse = ""
    if demande != "":
        id = virus_scan_url(demande)
        time.sleep(5)
        reponse = get_analyse_url(id)
    else:
        reponse = "Faire \"/virustotal <i>url</i>\" pour scanner une url"
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """
    Affiche le status de la raspberry.
    """
    dispatcher.add_handler(CommandHandler('virustotal', virustotal))
