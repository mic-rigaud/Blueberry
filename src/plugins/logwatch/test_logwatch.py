# @Author: michael
# @Date:   31-Mar-2020
# @Filename: test_logwatch.py
# @Last modified by:   michael
# @Last modified time: 31-Mar-2020
# @License: GNU GPL v3


import config as cfg
import pytest

from plugins.logwatch.logwatch import logwatch_liste


def test_logwatch():
    # Tests positifs
    result = logwatch_liste()
    assert result != "Probleme avec les logs"
    assert result != ""
