# @Author: michael
# @Date:   09-Feb-2018
# @Project: Major_Home
# @Filename: cartographie.py
# @Last modified by:   michael
# @Last modified time: 03-Jun-2019
# @License: GNU GPL v3

"""Cartographie le réseau."""

from api.Restricted import restricted
from scapy.all import ICMP, IP, conf, sr
from telegram.ext import CommandHandler


def ping():
    # Il faut les droits root pour scapy...
    conf.verb = 0
    rang = '192.168.1.1-255'
    rep, non_rep = sr(IP(dst=rang) / ICMP(), timeout=0.5)
    for elem in rep:
        if elem[1].type == 0:  # 0 <=> echo-reply
            print(
                elem[1].src + ' a renvoye un echo-reply au ping vers ' + str(elem[0].dst))


@restricted
def cartographie(bot, update):
    """Dit cartographie."""
    ping()
    bot.send_message(chat_id=update.message.chat_id,
                     text="Voici la cartographie de votre réseau")


def add(dispatcher):
    """
    Dit cartographie.

    Sans argument
    """
    handler = CommandHandler('carto', cartographie)
    dispatcher.add_handler(handler)
