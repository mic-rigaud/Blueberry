# @Author: michael
# @Date:   29-Sep-2019
# @Filename: test_nids_tools.py
# @Last modified by:   michael
# @Last modified time: 11-Jan-2020
# @License: GNU GPL v3

import pytest

from plugins.status import (status_cpu, status_ram, status_str,
                            status_suricata, temperature_raspberry)


def test_status_cpu():
    cpu = status_cpu()
    assert isinstance(cpu, str)


def test_status_ram():
    ram = status_ram()
    assert isinstance(ram, str)


def test_status_suricata():
    pid = status_suricata()
    assert isinstance(pid, str)


def test_temperature_raspberry():
    temp = temperature_raspberry()
    assert isinstance(temp, str)


def test_status_str():
    temp = status_str()
    assert isinstance(temp, str)
