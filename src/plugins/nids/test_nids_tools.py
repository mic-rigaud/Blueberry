# @Author: michael
# @Date:   29-Sep-2019
# @Filename: test_nids_tools.py
# @Last modified by:   michael
# @Last modified time: 15-Mar-2020
# @License: GNU GPL v3

import config as cfg

from src.plugins.nids.NidsTools import NidsTools


def test_get_last_log():
    # Tests positifs
    logs = NidsTools(cfg.suricata_log).get_last_log(3600)
    assert isinstance(logs, list)
    assert logs != []

    # Tests négatifs
    logs = NidsTools("fichier introuvable").get_last_log(3600)
    assert "[ERROR] Fichier" in logs

    logs = NidsTools(cfg.suricata_log).get_last_log("toto")
    assert "[ERROR] Exception" in logs

    logs = NidsTools(cfg.suricata_log).get_last_log(0)
    assert isinstance(logs, list)
    assert logs == []


def test_parse_event():
    assert True
