# @Author: michael
# @Date:   01-Jan-1970
# @Filename: BDD.py
# @Last modified by:   michael
# @Last modified time: 06-Feb-2021
# @License: GNU GPL v3
from peewee import BooleanField, CharField, DateTimeField, IntegerField, Model
from playhouse.sqlite_ext import SqliteDatabase

db = SqliteDatabase("./network.db")


class BaseModel(Model):
    """Classe BaseModel."""

    class Meta:
        """Classe Meta."""

        database = db
