# @Author: michael
# @Date:   09-Feb-2018
# @Project: Major_Home
# @Filename: cartographie.py
# @Last modified by:   michael
# @Last modified time: 16-Aug-2019
# @License: GNU GPL v3

"""Cartographie le réseau."""

import datetime
import logging
import socket

import config as cfg
import schedule
from api.api_bdd import Ip
from scapy.all import ICMP, IP, conf, srp


def ping():
    conf.verb = 0
    rang = '192.168.1.1-255'
    rep, non_rep = srp(IP(dst=rang) / ICMP(), timeout=0.5)
    for elem in rep:
        if elem[1].type == 0:  # 0 <=> echo-reply
            add_element(elem[0].dst)
        else:
            remove_element(elem[0].dst)


def get_hostname(ip):
    return socket.gethostbyaddr(ip)[0]


def remove_element(dst_ip):
    record = Ip.select().where((Ip.ip == dst_ip))
    if record.exists():
        element = record.get()
        element.satus = False
        element.save()


def add_element(dst_ip):
    dst_host = get_hostname(dst_ip)
    record = Ip.select().where((Ip.ip == dst_ip) & (Ip.host == dst_host))
    if record.exists():
        element = record.get()
        element.time_last = datetime.datetime.now()
        element.save()
    else:
        Ip.create(ip=dst_ip, host=dst_host).save()
        print("Ajout du couple: {}, {}".format(dst_host, dst_ip))
        flush()
        # send_alert(str(self.host), mac)


def cartographie():
    """Lance la cartographie."""
    ping()


def add():
    """Ajout la fonction cartographie."""
    schedule.every(cfg.cart_freq).hour.do(cartographie)
    cartographie()
