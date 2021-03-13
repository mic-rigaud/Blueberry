# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    nids_tools.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: michael <michael@mic-rigaud.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/12 12:26:07 by michael           #+#    #+#              #
#    Updated: 2021/03/12 12:26:44 by michael          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import logging

import config as cfg
from src.api.send_alert import send_alert
from src.plugins.nids.NidsTools import NidsTools


def nids_mqalert(context):
    """Creer une alerte lorsque suricata nous envoi"""
    messages = nids_alert()
    if "Il n'y a pas" not in messages[0]:
        for message in messages:
            send_alert(context, message)


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


def nids_alert():
    message = []
    evenements = NidsTools(cfg.suricata_log).get_last_log(cfg.freq_nids)
    if not evenements:
        return ["Il n'y a pas d'évènements"]
    if "[ERROR]" in evenements:
        return ["Il y a le problème suivant:\n " + str(evenements)]
    for event in evenements:
        if (
                event["event_type"] == "alert"
                and event["alert"]["category"] != "Not Suspicious Traffic"
        ):
            message_test = str(event).replace('\n', '')
            if message_test != "":
                message.append(message_test)
    if not message:
        return ["Il n'y a pas d'alertes"]
    return message
