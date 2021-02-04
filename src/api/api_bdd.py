# @Author: michael
# @Date:   28-Oct-2017
# @Project: Blueberry
# @Filename: api_bdd.py
# @Last modified by:   michael
# @Last modified time: 04-Feb-2021
# @License: GNU GPL v3

import datetime
import logging

import config as cfg
from peewee import BooleanField, CharField, DateTimeField, Model
from playhouse.sqlite_ext import SqliteDatabase

db = SqliteDatabase(cfg.work_dir + 'network.db')


class BaseModel(Model):
    """Classe BaseModel."""

    class Meta:
        """Classe Meta."""

        database = db


class Ip(BaseModel):
    """Objet definissant une IP pour la BDD."""

    ip = CharField()
    mac = CharField()
    hostname = CharField()
    time_first = DateTimeField(default=datetime.datetime.now)
    time_last = DateTimeField(default=datetime.datetime.now)
    confiance = BooleanField(default=False)
    status = BooleanField(default=True)
    ip_voisin = CharField(default="")

    def str_compact(self):
        if self.hostname != "unknown":
            return str(self.hostname)
        return str(self.ip)

    def isonline(self):
        self.time_last = datetime.datetime.now()

    def __str__(self):
        reponse = "<b>{}</b>\n\n".format(str(self.ip))
        reponse += "Nom : {}\n".format(str(self.hostname))
        reponse += "Mac : {}\n\n".format(str(self.mac))
        reponse += "Première connexion : {}\n".format(str(self.time_first))
        reponse += "Dernière connexion : {}\n".format(str(self.time_last))
        reponse += "IP du voisin : {}\n".format(str(self.ip_voisin))
        reponse += "Confiance : {}\n".format(str(self.confiance))
        return reponse


def get_info(id, Table):
    try:
        element_selected = Table.get(Table.id == id)
        return element_selected.__str__()
    except Exception as e:
        logging.warning(e)


def del_element(id, Table):
    try:
        Table.delete().where(Table.id == id).execute()
        return "Suppression avec succes"
    except Exception as e:
        logging.warning(e)

# class Parametres(BaseModel):
#     """Objet definissant un Parametres pour la BDD."""
#
#     section = CharField()
#     key = CharField(unique=True)
#     value = CharField()


#
# class Task(BaseModel):
#     action = CharField()
#     time = DateTimeField(default=datetime.datetime.now)
