# @Author: michael
# @Date:   08-May-2020
# @Filename: observatory.py
# @Last modified by:   michael
# @Last modified time: 11-May-2020
# @License: GNU GPL v3


"""Scan une adresse url via observatory."""

import json
import logging
import time

import config as cfg
import psutil
import requests
import telegram
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from api.Restricted import restricted

ADRESSE_HTTP_ANALYZE = "https://http-observatory.security.mozilla.org/api/v1/analyze?host="
ADRESSE_HTTP_SCAN = "https://http-observatory.security.mozilla.org/api/v1/getScanResults?scan="
ADRESSE_TLS_SCAN = "https://tls-observatory.services.mozilla.com/api/v1/scan?target="
ADRESSE_TLS_RESULT = "https://tls-observatory.services.mozilla.com/api/v1/results?id="


def print_analyse(url, analyse):
    try:
        reponse = "<b>{}</b>\n".format(url)
        reponse += "------ HTTP ------\n"
        reponse += "<b>Note  :</b> {}\n".format(analyse["grade"])
        reponse += "<b>Score :</b> {}/100\n".format(analyse["score"])
        reponse += "------------------\n"
        return reponse
    except KeyError:
        logging.error("Analyse retournée par observatory erronée")
        return "[ERROR] analyse fourni par observatory inexploitable"


def print_scan(scan):
    try:
        reponse = ""
        for element in scan:
            if scan[element]["score_modifier"] != 0:
                reponse += "• <b>{}</b> ({})\n{}\n".format(scan[element]["name"],
                                                           scan[element]["score_modifier"],
                                                           scan[element]["score_description"])
        return reponse
    except KeyError:
        logging.error("Result retournée par observatory erronée")
        return "[ERROR] Result fourni par observatory inexploitable"
    except TypeError:
        logging.error("Result retournée par observatory erronée")
        return "[ERROR] Result fourni par observatory inexploitable"


def get_icon(value):
    if value:
        return "✅"
    return "❌"


def print_tls_result(result):
    try:
        reponse = "\n------ TLS ------\n"
        reponse += "<b>tls</b>: {}\n".format(get_icon(result["has_tls"]))
        reponse += "<b>valide</b>: {}\n".format(get_icon(result["is_valid"]))
        reponse += "<b>IP:</b> {}\n".format(result["connection_info"]["scanIP"])
        return reponse
    except KeyError:
        logging.error("Analyse retournée par observatory erronée")
        return "[ERROR] analyse fourni par observatory inexploitable"


def get_id(analyse):
    return str(analyse["scan_id"])


def get_scan_url(id):
    req = requests.get(ADRESSE_HTTP_SCAN + id)
    scan = json.loads((req.content).decode("utf-8"))
    return scan


def get_analyse_url(url):
    req = requests.post(ADRESSE_HTTP_ANALYZE + url)
    time.sleep(1)
    req = requests.get(ADRESSE_HTTP_ANALYZE + url)
    analyse = json.loads((req.content).decode("utf-8"))
    return analyse


def get_scan_tls(url):
    req = requests.post(ADRESSE_TLS_SCAN + url)
    analyse = json.loads((req.content).decode("utf-8"))
    return analyse


def get_result_tls(id):
    req = requests.get(ADRESSE_TLS_RESULT + id)
    analyse = json.loads((req.content).decode("utf-8"))
    return analyse


def get_http_observatory(url):
    analyse = get_analyse_url(url)
    if "error" in analyse:
        return analyse["error"]
    scan = get_scan_url(get_id(analyse))
    return print_analyse(url, analyse) + print_scan(scan)


def get_tls_observatory(url):
    analyse = get_scan_tls(url)
    result = get_result_tls(get_id(analyse))
    return print_tls_result(result)


@restricted
def observatory(update: Update, context: CallbackContext):
    """Scan une adresse url via observatory."""
    demande = ' '.join(context.args).lower().split(" ")[0]
    reponse = ""
    if demande != "":
        reponse = get_http_observatory(demande)
        if demande in reponse:
            reponse += get_tls_observatory(demande)
    else:
        reponse = "Faire \"/observatory <i>url</i>\" pour scanner une url"
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """
    Scan une adresse url via observatory.
    """
    dispatcher.add_handler(CommandHandler('observatory', observatory))
