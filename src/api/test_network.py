# @Author: michael
# @Date:   03-Apr-2020
# @Filename: test_carto.py
# @Last modified by:   michael
# @Last modified time: 09-Feb-2021
# @License: GNU GPL v3

from src.api.network import get_myip, traceroute


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
