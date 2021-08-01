# @Author: michael
# @Date:   29-Sep-2019
# @Filename: test_nids_tools.py
# @Last modified by:   michael
# @Last modified time: 15-Mar-2020
# @License: GNU GPL v3

import config as cfg

from src.plugins.nids.NidsTools import NidsTools
from src.plugins.nids.nids_tools import find_country


def test_get_last_log():
    # Tests positifs
    logs = NidsTools(cfg.suricata_log).get_last_log(3600)
    assert isinstance(logs, list)
    assert logs != []

    # Tests négatifs
    logs = NidsTools("fichier introuvable").get_last_log(3600)
    assert "[ERROR][NIDS] Fichier" in logs

    logs = NidsTools(cfg.suricata_log).get_last_log("toto")
    assert "[ERROR][NIDS] Exception" in logs

    logs = NidsTools(cfg.suricata_log).get_last_log(0)
    assert isinstance(logs, list)
    assert logs == []


def test_parse_event():
    assert True


def test_find_country():
    country = find_country("8.8.8.8")
    assert country == "États-Unis"
    country = find_country("127.0.0.1")
    assert country == "NA"
