# @Author: michael
# @Date:   16-May-2020
# @Filename: test_scan.py
# @Last modified by:   michael
# @Last modified time: 16-May-2020
# @License: GNU GPL v3
from plugins.scan.scan import creer_bouton


def test_creer_bouton():
    assert "scan_tel" in str(creer_bouton("0600000000"))
    assert "scan_tel" in str(creer_bouton("118218"))

    assert "scan_wi" in str(creer_bouton("google.com"))
    assert "scan_wi" in str(creer_bouton("8.8.8.8"))

    assert "scan_vt" in str(creer_bouton("google.com"))
    assert "scan_vt" in str(creer_bouton("test.test.google.com"))
    assert "scan_vt" in str(creer_bouton("google@gmail.com"))

    assert "scan_ob" in str(creer_bouton("google.com"))
