import os
import shutil

import config as cfg

from plugins.nids.nids import nids_alert


def test_nids_alert():
    # Test avec une alerte
    messages = nids_alert()
    assert "alert" in messages[0]
    assert "[ERROR]" not in messages[0]

    # Test avec evenements mais sans alertes
    shutil.copy(cfg.suricata_log, cfg.suricata_log + ".old")
    text = ""
    with open(cfg.suricata_log, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "alert" in line:
                line = line.replace("alert", "flow")
            text += line
    with open(cfg.suricata_log, "w") as file:
        file.write(text)

    messages = nids_alert()
    assert messages[0] == "Il n'y a pas d'alertes"

    # Test sans fichier
    os.remove(cfg.suricata_log)
    messages = nids_alert()
    assert "[ERROR] Fichier" in messages[0]

    shutil.copy(cfg.suricata_log + ".old", cfg.suricata_log)
    os.remove(cfg.suricata_log + ".old")
