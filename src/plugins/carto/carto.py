# @Author: michael
# @Date:   31-Dec-2019
# @Filename: carto.py
# @Last modified by:   michael
# @Last modified time: 08-May-2020
# @License: GNU GPL v3


"""Envoie une carto """

import logging
from datetime import datetime
from subprocess import PIPE, Popen  # nosec

import config as cfg
import telegram
from graphviz import Digraph
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from api.api_bdd import Ip
from api.Restricted import restricted
from api.send_alert import send_alert


def get_myip():
    try:
        process = Popen(['/bin/ip', 'a'], stdout=PIPE, stderr=PIPE, shell=False)  # nosec
        stdout, stderr = process.communicate()
        if stderr.decode('utf8') != '':
            logging.warning(stderr.decode('utf8'))
        ip = stdout.decode('utf8').split('192.168')[1].split('/')[0]
        ip = "192.168" + ip
        return ip
    except IndexError:
        logging.error("Erreur avec la commande ip. Etes vous sur d'être connecté au réseau?")
        return "1.1.1.1"


def traceroute(ip):
    process = Popen(['/usr/bin/traceroute', '-m', '10', '-w',
                     '2', '-U', ip], stdout=PIPE, stderr=PIPE, shell=False)  # nosec
    stdout, stderr = process.communicate()
    if stderr.decode('utf8') != '':
        logging.warning(stderr.decode('utf8'))
    stdout = stdout.decode('utf8').split("\n")
    return stdout


def get_ip_voisin(ip):
    routes = traceroute(ip)
    if len(routes) == 3 and ip in routes[1]:
        return get_myip()
    elif len(routes) == 3 and ip not in routes[1]:
        return "None"
    elif len(routes) < 3:
        return "None"
    else:
        voisin = routes[len(routes) - 3]
        if "* * *" in voisin:
            return "None"
        return voisin.split('(')[1].split(')')[0]


def remplir_ip_voisin():
    reponse = ""
    for ip in Ip.select():
        ip_voisin = get_ip_voisin(ip.ip)
        reponse += ip_voisin + '\n'
        record = Ip.select().where((Ip.ip == ip.ip))
        element = record.get()
        element.ip_voisin = ip_voisin
        element.save()
    return reponse


def creer_carto():
    dict_ip_voisin = {}
    dot = Digraph(name='Network', format='png')
    dot.node(get_myip(), label="blueberry")
    for ip in Ip.select():
        if ip.ip_voisin != "None":
            if ip.hostname != "unknown":
                dot.node(ip.ip, label=ip.hostname)
            else:
                dot.node(ip.ip)
            if ip.ip_voisin in dict_ip_voisin:
                dict_ip_voisin[ip.ip_voisin] += 1
            else:
                dict_ip_voisin[ip.ip_voisin] = 1
    for ip in dict_ip_voisin:
        if dict_ip_voisin[ip] > 1:
            if ip == get_myip():
                dot.node('swicth-blueberry')
                dot.edge(ip, 'swicth-blueberry')
            else:
                dot.node('swicth-' + ip)
    for ip in Ip.select():
        if ip.ip_voisin != "None":
            if ip.ip_voisin in dict_ip_voisin and dict_ip_voisin[ip.ip_voisin] > 1:
                if ip.ip_voisin == get_myip():
                    dot.edge(ip.ip, 'swicth-blueberry')
                else:
                    dot.edge(ip.ip, 'swicth-' + ip.ip_voisin)
            else:
                dot.edge(ip.ip, ip.ip_voisin)
    dot.render()


@restricted
def carto(update: Update, context: CallbackContext):
    """Lance carto."""
    message = "Attention cela peut prendre un certain temps\n\n" +\
        "<i>Si le résultat attendu n'est pas satisfaisant c'est que soit:\n" +\
        "- traceroute ne fait pas bien son travail. Ce qui arrive malheureusement... \n" + \
        "- La base de donnée remplie par arpwatch est vide pour le moment." +\
        " Vous pouvez forcer un scan manuel avec la commande /arpwatch</i>"
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=message, parse_mode=telegram.ParseMode.HTML)
    remplir_ip_voisin()
    creer_carto()
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('Network.gv.png', 'rb'))


def add(dispatcher):
    """Ajout la fonction carto."""
    dispatcher.add_handler(CommandHandler('carto', carto, pass_job_queue=True))
    # start_veille(dispatcher.job_queue)
