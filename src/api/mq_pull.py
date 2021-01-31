# @Author: michael
# @Date:   01-Jan-1970
# @Filename: mq_pull.py
# @Last modified by:   michael
# @Last modified time: 31-Jan-2021
# @License: GNU GPL v3

import logging
from multiprocessing import Process

import config as cfg
import zmq
from telegram import ParseMode


def mqPull(updater):
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://127.0.0.1:5555")
    logging.info("Lancement de l'écoute d alerte")
    while True:
        recv = receiver.recv()
        task, message = str(recv).split("+")
        message = message.replace("\\n", "\n")
        logging.info("Reception de l'alerte : " + message)
        for chat_id in cfg.user:
            updater.bot.send_message(chat_id=chat_id,
                                     text=str(message),
                                     parse_mode=ParseMode.HTML)
