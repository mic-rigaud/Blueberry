# @Author: michael
# @Date:   01-Jan-1970
# @Filename: Ip.py
# @Last modified by:   michael
# @Last modified time: 09-Feb-2021
# @License: GNU GPL v3

from datetime import datetime

import config as cfg
from peewee import BooleanField, CharField, DateTimeField, FloatField, IntegerField

from src.api.BDD import BaseModel


class Ip(BaseModel):
    """Objet definissant une IP pour la BDD."""

    ip = CharField()
    mac = CharField()
    hostname = CharField()
    time_first = DateTimeField(default=datetime.now)
    time_last = DateTimeField(default=datetime.now)
    confiance = BooleanField(default=False)
    status = BooleanField(default=True)
    ip_voisin = CharField(default="")
    alias = CharField(default="")

    def str_compact(self):
        if self.status:
            result_icon = "✅ "
        else:
            result_icon = "❌ "
        if self.alias != "":
            return result_icon + str(self.alias)
        if self.hostname != "unknown":
            return result_icon + str(self.hostname)
        return result_icon + str(self.ip)

    def isonline(self):
        self.status = True
        self.time_last = datetime.now()

    def isoffline(self):
        self.status = False

    def __str__(self):
        reponse = "<b>{}</b>\n\n".format(str(self.ip))
        reponse += "Nom : {}\n".format(str(self.hostname))
        if self.alias != "":
            reponse += "Alias : {}\n".format(str(self.alias))
        reponse += "Mac : {}\n\n".format(str(self.mac))
        reponse += "Première connexion : {}\n".format(str(self.time_first))
        reponse += "Dernière connexion : {}\n".format(str(self.time_last))
        reponse += "IP du voisin : {}\n".format(str(self.ip_voisin))
        reponse += "Confiance : {}\n".format(str(self.confiance))
        return reponse
