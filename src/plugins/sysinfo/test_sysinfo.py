# @Author: michael
# @Date:   29-Sep-2019
# @Filename: test_nids_tools.py
# @Last modified by:   michael
# @Last modified time: 03-Apr-2020
# @License: GNU GPL v3

import pytest

from plugins.sysinfo.sysinfo import (status_cpu, status_ram, status_service,
                                     status_str, temperature_raspberry)


def test_status_cpu():
    cpu = status_cpu()
    assert isinstance(cpu, str)


def test_status_ram():
    ram = status_ram()
    assert isinstance(ram, str)


def test_status_service():
    pid = status_service("suricata")
    assert isinstance(pid, str)


def test_temperature_raspberry():
    temp = temperature_raspberry()
    assert isinstance(temp, str)


def test_status_str():
    temp = status_str()
    assert isinstance(temp, str)
