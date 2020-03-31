# @Author: michael
# @Date:   29-Sep-2019
# @Filename: test_nids_tools.py
# @Last modified by:   michael
# @Last modified time: 15-Mar-2020
# @License: GNU GPL v3

import pytest

from api.nids_tools import NidsTools

LOG = "./test/data/suricata-log.json"


def test_get_last_log():
    # Tests positifs
    logs = NidsTools(LOG).get_last_log(3600)
    assert isinstance(logs, list)
    assert logs != []

    # Tests négatifs
    with pytest.raises(FileNotFoundError):
        logs = NidsTools("fichier introuvable").get_last_log(3600)

    with pytest.raises(TypeError):
        logs = NidsTools(LOG).get_last_log("toto")

    logs = NidsTools(LOG).get_last_log(0)
    assert isinstance(logs, list)
    assert logs == []
