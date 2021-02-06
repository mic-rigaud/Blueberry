# @Author: michael
# @Date:   01-Jan-1970
# @Filename: carto_tools.py
# @Last modified by:   michael
# @Last modified time: 06-Feb-2021
# @License: GNU GPL v3

import logging

from graphviz import Digraph
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.api.button import build_menu
from src.api.network import get_myip, ping, traceroute
from src.plugins.carto.Ip import Ip


def creer_button_ip():
    button_list = []
    for ip in Ip.select():
        button_list.append(InlineKeyboardButton(
            ip.str_compact(), callback_data="carto_info_{}".format(ip.id)))
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


def carto_creer_button_info(id, filtre):
    button_list = []
    button_list.append(InlineKeyboardButton(
        "Ping", callback_data="carto_ping_{}_{}".format(id, filtre)))
    button_list.append(InlineKeyboardButton(
        "Scan", callback_data="carto_scan_{}_{}".format(id, filtre)))
    button_list.append(InlineKeyboardButton(
        "Supprimer", callback_data="carto_scan_{}_{}".format(id, filtre)))
    button_list.append(InlineKeyboardButton(
        "Retour", callback_data="carto_lister_{}".format(filtre)))
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))


def carto_ping(id):
    ip = Ip.get(Ip.id == id)
    if ping(ip.ip) == 0:
        ip.isonline()
        ip.save()
        return "La machine est en ligne"
    ip.isoffline()
    ip.save()
    return "La machine est hors ligne"


def carto_ping_all():
    logging.info("Demarrage du scan des adresses IP")
    for ip in Ip.select():
        carto_ping(ip.id)
    logging.info("Fin du scan des adresses IP")
    return "L'ensemble des Ip connues ont ete pingé"

#


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
