# @Author: michael
# @Date:   03-Apr-2020
# @Filename: test_carto.py
# @Last modified by:   michael
# @Last modified time: 03-Apr-2020
# @License: GNU GPL v3

from plugins.carto.carto import get_ip_voisin, get_myip, traceroute


def test_get_myip():
    ip = get_myip()
    assert ip != "192.168"


def test_traceroute(caplog):
    # Test positif
    route = traceroute("1.1.1.1")
    assert "traceroute" in route[0]

    # Test negatif
    route = traceroute("route_inconnu")
    for record in caplog.records:
        assert "route_inconnu:" in record.message


def test_get_ip_voisin():
    voisin = get_ip_voisin("1.1.1.1")
    assert voisin == "None"

    voisin = get_ip_voisin("route_inconnu")
    assert voisin == "None"
