# @Author: michael
# @Date:   31-Mar-2020
# @Filename: test_arpwatch.py
# @Last modified by:   michael
# @Last modified time: 31-Mar-2020
# @License: GNU GPL v3


import config as cfg
import pytest

from plugins.arpwatch.arpwatch import arpwatch_liste, parse


def test_parse():
    # Tests positifs
    line_test = ['---\n', 'From: arpwatch (Arpwatch Blueberry)\n', 'To: root\n', 'Subject: new station (DEBIAN) enp0s3\n', '\n', '            hostname: DEBIAN\n', '          ip address: 1.1.1.1\n',
                 '           interface: enp0s3\n', '    ethernet address: 00:00:00:00:11:11\n', '     ethernet vendor: PPP\n', '           timestamp: Tuesday, March 10, 2050 09:10:11 +0200\n']
    result = parse(line_test)
    assert result[0]["hostname"] == "DEBIAN"
    assert result[0]["ip"] == "1.1.1.1"
    assert result[0]["vendor"] == "PPP"
    assert result[0]["mac"] == "00:00:00:00:11:11"


def test_arpwatch():
    # Tests positifs
    result = arpwatch_liste()
    assert "[ERROR]" not in result
    assert result != ""
