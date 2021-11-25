# @Author: michael
# @Date:   02-Jun-2019
# @Filename: Restricted.py
# @Last modified by:   michael
# @Last modified time: 13-Nov-2019
# @License: GNU GPL v3


"""Creer le decorateur restricted."""
import logging
from functools import wraps

import config as cfg
from telegram import Update
from telegram.ext import CallbackContext


def restricted(func):
    """Rends les commandes en restricted."""

    @wraps(func)
    def wrapped(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id not in cfg.user:
            logging.info("Access non autorisé pour {}.".format(user_id))
            return
        return func(update, context)

    return wrapped
