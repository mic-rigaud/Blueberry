# @Author: michael
# @Date:   01-Jan-1970
# @Filename: arpwatch_tools.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3

import datetime
import logging

import config as cfg

from src.api.send_alert import send_alert
from src.plugins.arpwatch.ArpWatchError import ArpWatchError
from src.plugins.carto.Ip import Ip


def arpwatch_mqalert(context):
    try:
        elements = arpwatch_read()
        for i in elements:
            element = elements[i]
            if not isempty(element) and add_element(element):
                message = "Un nouvel appareil repéré sur le réseau:\n" + \
                    "{}  {}  {}\n".format(element["hostname"], element["ip"],
                                          element["timestamp"])
                send_alert(context, message)
    except ArpWatchError as exception:
        send_alert(context, str(exception))


def isempty(element):
    return element["hostname"] == "" and element["ip"] == "" and element["timestamp"] == ""


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
