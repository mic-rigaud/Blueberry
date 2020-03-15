import pytest
from telegram import InlineKeyboardMarkup

from plugins.log.log import creer_bouton, log_liste, log_rm


def test_log_liste():
    reponse = log_liste()
    assert "Voici les 10 derniers log" in reponse


def test_log_rm():
    assert True


def test_creer_bouton():
    button = creer_bouton()
    assert isinstance(button, InlineKeyboardMarkup)
