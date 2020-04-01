# @Author: michael
# @Date:   29-Sep-2019
# @Filename: test_nids_tools.py
# @Last modified by:   michael
# @Last modified time: 15-Mar-2020
# @License: GNU GPL v3

import config as cfg
import pytest

from plugins.nids.nids_tools import NidsTools


def test_get_last_log():
    # Tests positifs
    logs = NidsTools(cfg.suricata_log).get_last_log(3600)
    assert isinstance(logs, list)
    assert logs != []

    # Tests négatifs
    logs = NidsTools("fichier introuvable").get_last_log(3600)
    assert logs == "Fichier introuvable"

    logs = NidsTools(cfg.suricata_log).get_last_log("toto")
    assert logs == "Exception"

    logs = NidsTools(cfg.suricata_log).get_last_log(0)
    assert isinstance(logs, list)
    assert logs == []
