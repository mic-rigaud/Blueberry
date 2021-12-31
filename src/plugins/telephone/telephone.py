# @Author: michael
# @Date:   13-May-2020
# @Filename: telephone.py
# @Last modified by:   michael
# @Last modified time: 16-May-2020
# @License: GNU GPL v3

"""Scan un numéro de téléphone."""

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

ADRESSE_SVA = "https://www.infosva.org/?tel="
ADRESSE_PAGEJAUNE = "https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui="


def parse_sva(soup):
    message = soup.find_all("tbody")
    lignes = message[0].find_all("tr")
    reponse = "<b><u>Service à Valeur Ajoutée</u></b>\n\n"
    for ligne in lignes:
        colonnes = ligne.find_all("td")
        reponse += "<b>{}</b> : {}\n".format(
            colonnes[0].get_text().replace("\n", ""),
            colonnes[1].get_text().replace("\n", ""),
        )
        reponse = reponse.replace("  ", "").replace("(données au", " (données au")
    return reponse


def parse_pj(soup):
    result = soup.find_all("section", "results")
    vcards = result[0].find_all("header", "v-card")
    reponse = ""
    for element in vcards:
        souselement = element.find_all("a")
        reponse += "• "
        for info in souselement:
            reponse += info.get_text().replace("\n", " ") + "\n"
    if reponse == "":
        reponse = "Il n'y a pas de résultats"
    return reponse


def sva_analyse(tel):
    today = datetime.now()
    r = requests.get(ADRESSE_SVA + tel + "&date=" + today.strftime("%d-%m-%Y"))
    soup = BeautifulSoup(r.text, "html.parser")
    return parse_sva(soup)


def pj_analyse(tel):
    r = requests.get(ADRESSE_PAGEJAUNE + tel + "&univers=annuaireinverse&idOu=")
    soup = BeautifulSoup(r.text, "html.parser")
    return parse_pj(soup)


def get_analyse(tel):
    re_sva = re.compile("08[0-9]+")
    re_sva2 = re.compile("118[0-9]+")
    re_sva3 = re.compile("[3,1][0-9]+")
    if re_sva.match(tel) or re_sva2.match(tel) or re_sva3.match(tel):
        return sva_analyse(tel)
    return pj_analyse(tel)


def telephone(update: Update, context: CallbackContext):
    """Scan un numéro de téléphone."""
    demande = " ".join(context.args).lower().split(" ")[0]
    reply_markup = None
    reponse = get_analyse(demande)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=reponse,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


def add(dispatcher):
    """
    Scan un numéro de téléphone.
    """
    dispatcher.add_handler(CommandHandler("telephone", telephone))
