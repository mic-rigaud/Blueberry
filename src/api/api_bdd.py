# @Author: michael
# @Date:   28-Oct-2017
# @Project: Blueberry
# @Filename: api_bdd.py
# @Last modified by:   michael
# @Last modified time: 03-Apr-2020
# @License: GNU GPL v3

import datetime

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
