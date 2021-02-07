# @Author: michael
# @Date:   01-Jan-1970
# @Filename: mq_pull.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3

import logging
from multiprocessing import Process

import config as cfg
import zmq
from telegram import ParseMode

from src.plugins.arpwatch.arpwatch_tools import arpwatch_mqalert


def mqPull(updater):
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://127.0.0.1:5555")
    logging.info("Lancement de l'écoute d alerte")
    while True:
        recv = receiver.recv()
        task, message = str(recv).split("+")
        if "arpwatch" in str(task):
            logging.info("Reception d'une alerte arpwatch")
            arpwatch_mqalert(updater)
        elif "hids" in str(task):
            message = message.replace("\\n", "\n")
            logging.info("Reception de l'alerte : " + message)
            for chat_id in cfg.user:
                updater.bot.send_message(chat_id=chat_id,
                                         text=str(message),
                                         parse_mode=ParseMode.HTML)
        else:
            logging.info("Erreur task inconnu : {}".format(str(task)))
