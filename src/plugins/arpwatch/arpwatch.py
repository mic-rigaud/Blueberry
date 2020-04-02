# @Author: michael
# @Date:   31-Mar-2020
# @Filename: arpwatch.py
# @Last modified by:   michael
# @Last modified time: 02-Apr-2020
# @License: GNU GPL v3


"""Affiche la base arpwatch et alerte lors d'une nouvelle entrée."""

import datetime
import logging

import config as cfg
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from api.api_bdd import Ip
from api.button import build_menu
from api.Restricted import restricted
from api.send_alert import send_alert
from plugins.arpwatch.ArpWatchError import ArpWatchError


def job_veille(context):
    """Affiche les alarmes."""
    try:
        elements = arpwatch_read()
        for i in elements:
            element = elements[i]
            if add_element(element):
                message = "Un nouvel appareil repéré sur le réseau:\n" + \
                    "{}  {}  {}\n".format(element["hostname"], element["ip"],
                                          element["timestamp"])
                send_alert(context, message)
    except ArpWatchError as exception:
        send_alert(context, str(exception))


def start_veille(job_queue):
    """Lance la veille."""
    heures = int(cfg.freq_arpwatch.split("h")[0])
    minutes = int(cfg.freq_arpwatch.split("h")[1])
    datetime_heure = datetime.time(heures, minutes)
    job_queue.run_daily(job_veille,
                        datetime_heure,
                        name="veille_arpwatch")
    logging.info("Veille lancé")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = "La veille n'est pas lancé.\n"
    job = job_queue.get_jobs_by_name("veille_arpwatch")
    for j in job:
        if not j.removed:
            reponse = "La veille est lancé.\n" +\
                "Un scan est réalisé tous les jours à " + cfg.freq_arpwatch
    return reponse


def arpwatch_liste():
    try:
        reponse = ""
        contenu = arpwatch_read()
        for i in contenu:
            element = contenu[i]
            reponse += "{}  {}  {}\n".format(element["hostname"], element["ip"],
                                             element["timestamp"])
        reponse = reponse.replace("<", "").replace(">", "")
        return reponse
    except ArpWatchError as exception:
        return str(exception)


def arpwatch_read():
    """Cette fonction permet de gerer les erreurs."""
    try:
        with open(cfg.arpwatch_mail, 'r') as file:
            return parse(file.readlines())
    except PermissionError:
        logging.error("Permission Error")
        raise ArpWatchError(
            "[ERROR] Vous n'avez pas les droits sur le fichier " + cfg.arpwatch_mail)
    except FileNotFoundError as exception:
        logging.error(exception)
        raise ArpWatchError(
            "[ERROR] Fichier {} introuvable - Etes vous sur que arpwatch fonctionne? Reesayez dans quelques secondes.".format(cfg.arpwatch_mail))
    except Exception as exception:
        logging.warning(exception)
        raise ArpWatchError("[ERROR] Exception - " + str(exception))


def parse(lines):
    """Cette fonction parse le format de mail de arpwatch."""
    retour = {}
    i = -1
    for line in lines:
        if line == "---\n":
            i += 1
            retour[i] = {"hostname": "",
                         "ip": "",
                         "vendor": "",
                         "timestamp": "",
                         "mac": ""}
        elif "hostname" in line:
            retour[i]["hostname"] = line.split(': ')[1].replace(
                '\n', '').replace('<', '').replace('>', '')
        elif "ip address" in line:
            retour[i]["ip"] = line.split(': ')[1].replace('\n', '')
        elif "ethernet vendor" in line:
            retour[i]["vendor"] = line.split(': ')[1].replace('\n', '')
        elif "timestamp" in line:
            timestamp = line.split(': ')[1].replace('\n', '')
            datetime_time = datetime.datetime.strptime(timestamp, "%A, %B %d, %Y %H:%M:%S %z")
            retour[i]["timestamp"] = datetime_time.strftime("%d/%m/%y-%X")
        elif "ethernet address" in line:
            retour[i]["mac"] = line.split(': ')[1].replace('\n', '')
    return retour


def add_element(element):
    """Ajoute l'élément à la base de donnée pour traitement."""
    record = Ip.select().where((Ip.ip == element["ip"]) & (Ip.mac == element["mac"]))
    if not record.exists():
        date = datetime.datetime.strptime(element["timestamp"], "%d/%m/%y-%X")
        Ip.create(ip=element["ip"], mac=element["mac"],
                  time_first=date, hostname=element["hostname"]).save()
        logging.info("Ajout du couple: {}, {}".format(element["mac"], element["ip"]))
        return True
    return False

###############################################################################


def creer_bouton():
    """Creer la liste de boutons."""
    button_list = [
        InlineKeyboardButton("afficher", callback_data="arpwatch_liste"),
        InlineKeyboardButton("etat job", callback_data="arpwatch_job"),
        ]
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def button_liste(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = arpwatch_liste()
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


def button_job(update: Update, context: CallbackContext):
    query = update.callback_query
    reply_markup = creer_bouton()
    reponse = get_info_veille(context.job_queue)
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=reponse,
                                  parse_mode=telegram.ParseMode.HTML,
                                  reply_markup=reply_markup)


@restricted
def arpwatch(update: Update, context: CallbackContext):
    """Affiche la base arpwatch et alerte lors d'une nouvelle entrée."""
    reponse = "Que puis-je faire pour vous?"
    reply_markup = creer_bouton()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML,
                             reply_markup=reply_markup)


def add(dispatcher):
    """
    Affiche la base arpwatch et alerte lors d'une nouvelle entrée.
    """
    dispatcher.add_handler(CommandHandler('arpwatch', arpwatch, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(button_job, pattern="^arpwatch_job$"))
    dispatcher.add_handler(CallbackQueryHandler(button_liste, pattern="^arpwatch_liste$"))
    start_veille(dispatcher.job_queue)
