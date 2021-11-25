# @Author: michael
# @Date:   01-Jan-1970
# @Filename: test_carto_tools.py
# @Last modified by:   michael
# @Last modified time: 09-Feb-2021
# @License: GNU GPL v3


from datetime import datetime

from src.plugins.carto.carto_tools import get_ip_voisin
from src.plugins.carto.Ip import Ip


def test_get_ip_voisin():
    voisin = get_ip_voisin("1.1.1.1")
    assert voisin == "None"

    voisin = get_ip_voisin("route_inconnu")
    assert voisin == "None"


def test_str_compact():
    ip = Ip.create(
        ip="1.1.1.1",
        mac="xxx.xxx.xxx.xxx",
        time_first=datetime.now(),
        hostname="hello",
        status=True,
    )
    assert "hello" in ip.str_compact()
    assert "hello" in ip.str_compact()

    ip = Ip.create(
        ip="1.1.1.1",
        mac="xxx.xxx.xxx.xxx",
        time_first=datetime.now(),
        hostname="unknown",
        status=False,
    )
    assert "1.1.1.1" in ip.str_compact()
    assert "❌" in ip.str_compact()

    ip = Ip.create(
        ip="1.1.1.1",
        mac="xxx.xxx.xxx.xxx",
        time_first=datetime.now(),
        hostname="hello",
        alias="bonjour",
    )
    assert "bonjour" in ip.str_compact()
