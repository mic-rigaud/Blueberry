# @Author: michael
# @Date:   01-Jan-1970
# @Filename: topo_tools.py
# @Last modified by:   michael
# @Last modified time: 04-Feb-2021
# @License: GNU GPL v3

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.api.api_bdd import Ip
from src.api.button import build_menu


def creer_button_ip():
    button_list = []
    for ip in Ip.select():
        button_list.append(InlineKeyboardButton(
            ip.str_compact(), callback_data="topo_info_{}".format(ip.id)))
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=1))


def creer_button_info(id):
    button_list = []
    button_list.append(InlineKeyboardButton("Ping", callback_data="topo_ping_{}".format(id)))
    button_list.append(InlineKeyboardButton("Scan", callback_data="topo_scan_{}".format(id)))
    return InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
