# @Author: michael
# @Date:   23-Apr-2020
# @Filename: whois.py
# @Last modified by:   michael
# @Last modified time: 29-Apr-2020
# @License: GNU GPL v3


"""Analyse une url avec whois."""

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

ADRESSE = "https://www.whoisxmlapi.com/whoisserver/WhoisService?outputFormat=json&apiKey=" + cfg.whois_key


def print_analyse(analyse):
    try:
        if "ErrorMessage" in analyse:
            return analyse["ErrorMessage"]["msg"]

        if "registrant" in analyse["WhoisRecord"]["registryData"]:
            informations = analyse["WhoisRecord"]["registryData"]
        else:
            informations = analyse["WhoisRecord"]

        reponse = "--- <b>Général</b> ---\n"
        reponse += "Nom: {}\n".format(analyse["WhoisRecord"]["domainName"])
        if "createdDateNormalized" in informations:
            reponse += "Date de création: {}\n".format(informations["createdDateNormalized"])
        if "updatedDateNormalized" in informations:
            reponse += "Dernier update: {}\n".format(informations["updatedDateNormalized"])
        if "expiresDateNormalized" in informations:
            reponse += "Date d'expiration: {}\n".format(informations["expiresDateNormalized"])
        if "registrarName" in informations:
            reponse += "Nom de registre: {}\n".format(informations["registrarName"])

        if "registrant" in informations:
            reponse += "\n--- <b>Inscrit</b> ---\n"
            if "name" in informations["registrant"]:
                reponse += "Contact: {}\n".format(informations["registrant"]["name"])
            if "organization" in informations["registrant"]:
                reponse += "Organisation: {}\n".format(informations["registrant"]["organization"])
            reponse += "Pays: {}\n".format(informations["registrant"]["country"])
            if "email" in informations["registrant"]:
                reponse += "Email: {}\n".format(informations["registrant"]["email"])

        if "administrativeContact" in informations:
            reponse += "\n--- <b>Organisation</b> ---\n"
            if "organization" in informations["administrativeContact"]:
                reponse += "Contact: {}\n".format(
                    informations["administrativeContact"]["organization"])
            if "country" in informations["administrativeContact"]:
                reponse += "Pays: {}\n".format(informations["administrativeContact"]["country"])
            if "email" in informations["administrativeContact"]:
                reponse += "Email: {}\n".format(informations["administrativeContact"]["email"])

        if "technicalContact" in informations:
            reponse += "\n--- <b>Contact Technique</b> ---\n"
            if "organization" in informations["technicalContact"]:
                reponse += "Contact: {}\n".format(informations["technicalContact"]["organization"])
            if "country" in informations["technicalContact"]:
                reponse += "Pays: {}\n".format(informations["technicalContact"]["country"])
            if "email" in informations["technicalContact"]:
                reponse += "Email: {}\n".format(informations["technicalContact"]["email"])

        if "nameServers" in informations:
            reponse += "\n--- <b>Noms des serveurs</b> ---\n"
            reponse += "{}".format(informations["nameServers"]["rawText"])

        return reponse
    except KeyError as e:
        logging.error("Analyse retournée par whois erronée")
        print(e)
        return "[ERROR] analyse fourni par whois inexploitable"


def get_whois(domain):
    req = requests.get(ADRESSE + "&domainName=" + domain)
    analyse = json.loads((req.content).decode("utf-8"))
    return print_analyse(analyse)


@restricted
def whois(update: Update, context: CallbackContext):
    """Affiche le status de la raspberry."""
    demande = ' '.join(context.args).lower().split(" ")[0]
    reponse = ""
    if demande != "":
        reponse = get_whois(demande)
    else:
        reponse = "Faire \"/whois <i>domain/ip/email</i>\""
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """
    Renvoi un whois.
    """
    if cfg.whois_key != "0":
        dispatcher.add_handler(CommandHandler('whois', whois))
