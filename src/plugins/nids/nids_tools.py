# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nids_tools.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: michael <michael@mic-rigaud.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/12 12:26:07 by michael           #+#    #+#              #
#    Updated: 2021/03/27 14:40:02 by michael          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging
from datetime import datetime

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
        country = "NA"
        http = event["http"] if "http" in event else "NA"
        return f"<b>{event['alert']['signature']}</b>\n" \
               f"time :{time.strftime('%H:%M:%S')}\n" \
               f"src : {event['src_ip']} ({country})\ndst : {event['dest_ip']}\n" \
               f"signature id : {event['alert']['signature_id']}\n" \
               f"category : {event['alert']['category']}\nhttp : {http}"
    except Exception as excep:
        logging.warning(str(excep))
        return str(event)


def nids_alert():
    evenements = NidsTools(cfg.suricata_log).get_last_log(cfg.freq_nids)
    if not evenements:
        return ["Il n'y a pas d'évènements"]
    if "[ERROR]" in evenements:
        return ["Il y a le problème suivant:\n " + str(evenements)]
    message = [parse_event(event) for event in evenements if (
            event["event_type"] == "alert"
            and event["alert"]["category"] != "Not Suspicious Traffic"
    ) and str(event).replace('\n', '') != ""]
    if not message:
        return ["Il n'y a pas d'alertes"]
    return message
