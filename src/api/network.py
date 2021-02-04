# @Author: michael
# @Date:   01-Jan-1970
# @Filename: network.py
# @Last modified by:   michael
# @Last modified time: 04-Feb-2021
# @License: GNU GPL v3


import logging
from subprocess import PIPE, Popen  # nosec


def get_myip():
    try:
        process = Popen(['/bin/ip', 'a'], stdout=PIPE, stderr=PIPE, shell=False)  # nosec
        stdout, stderr = process.communicate()
        if stderr.decode('utf8') != '':
            logging.warning(stderr.decode('utf8'))
        ip = stdout.decode('utf8').split('192.168')[1].split('/')[0]
        ip = "192.168" + ip
        return ip
    except IndexError:
        logging.error("Erreur avec la commande ip. Etes vous sur d'être connecté au réseau?")
        return "1.1.1.1"


def traceroute(ip):
    process = Popen(['/usr/bin/traceroute', '-m', '10', '-w',
                     '2', '-U', ip], stdout=PIPE, stderr=PIPE, shell=False)  # nosec
    stdout, stderr = process.communicate()
    if stderr.decode('utf8') != '':
        logging.warning(stderr.decode('utf8'))
    stdout = stdout.decode('utf8').split("\n")
    return stdout


def ping(ip):
    process = Popen(['/bin/ping', '-c', '5', ip], stdout=PIPE,
                    stderr=PIPE, shell=False)  # nosec
    stdout, stderr = process.communicate()
    if stderr.decode('utf8') != '':
        logging.warning(stderr.decode('utf8'))
    return process.returncode
