# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nids_tools.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: michael <michael@mic-rigaud.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/12 12:26:07 by michael           #+#    #+#              #
#    Updated: 2021/08/04 21:37:18 by michael          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging
from datetime import datetime

from geolite2 import geolite2

import config as cfg
from src.api.send_alert import send_alert
from src.plugins.nids.NidsTools import NidsTools


def nids_mqalert(context):
    """Creer une alerte lorsque suricata nous envoi"""
    logging.error("Fonction non encore implementé")


def job_veille(context):
    """Affiche les alarmes."""
    messages = nids_alert()
    if "Il n'y a pas" not in messages[0]:
        for message in messages:
            send_alert(context, message)


def start_veille(job_queue):
    """Lance la veille."""
    job_queue.run_repeating(job_veille,
                            cfg.freq_nids,
                            first=5,
                            name="veille_nids")
    logging.info("Veille lancé")
    return "Veille Lancé"


def get_info_veille(job_queue):
    """Indique si le job est lancé."""
    reponse = "La veille n'est pas lancé.\n"
    job = job_queue.get_jobs_by_name("veille_nids")
    for j in job:
        if not j.removed:
            reponse = "La veille est lancé.\n"
    return reponse


def parse_event(event):
    try:
        if "alert" not in event:
            return str(event).replace('\n', '')
        time = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
        country = find_country(event['src_ip'])
        http = event["http"] if "http" in event else "NA"
        return f"<b>{event['alert']['signature']}</b>\n" \
               f"time :{time.strftime('%H:%M:%S')}\n" \
               f"src : {event['src_ip']} ({country})\ndst : {event['dest_ip']}\n" \
               f"signature id : {event['alert']['signature_id']}\n" \
               f"category : {event['alert']['category']}\nhttp : {http}"
    except Exception as excep:
        logging.warning(str(excep))
        return str(event)


def find_country(ip: str) -> str:
    reader = geolite2.reader()
    match = reader.get(ip)
    if not match:
        return 'NA'
    if 'country' in match:
        return match['country']['names']['fr']
    else:
        return match['continent']['names']['fr']


def nids_alert(all=False):
    evenements = NidsTools(cfg.suricata_log).get_last_log(cfg.freq_nids)
    if not evenements:
        return ["Il n'y a pas d'évènements"]
    if "[ERROR]" in evenements:
        return ["Il y a le problème suivant:\n " + str(evenements)]
    message = [parse_event(event) for event in evenements if (
        is_relevant(event, all)
    ) and str(event).replace('\n', '') != ""]
    if not message:
        return ["Il n'y a pas d'alertes"]
    return message


def is_relevant(event: dict, all: bool) -> bool:
    if all:
        if event["event_type"] == "alert" and event["alert"]["category"] != "Not Suspicious Traffic":
            return True
    else:
        if event["event_type"] == "alert" and event["alert"]["category"] != "Not Suspicious Traffic":
            if not cfg.nids_exclude_scan:
                return is_relevant_filter(event)
            if "SCAN" not in event['alert']['signature']:
                return is_relevant_filter(event)
        return False


def is_relevant_filter(event: dict) -> bool:
    """filtre_event: filtre les evenements qui respectent les regles définis dans config.py"""
    regle = cfg.nids_filtre_rule.copy()
    for key in regle:
        event_temp = event.copy()
        regle_temp = regle.copy()[key]
        while type(regle_temp) == dict:
            if list(regle_temp.keys())[0] not in event_temp:
                break
            event_temp = event_temp[list(regle_temp.keys())[0]]
            regle_temp = regle_temp[list(regle_temp.keys())[0]]
        else:
            if regle_temp in event_temp:
                return False
    return True
