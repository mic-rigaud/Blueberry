# @Author: michael
# @Date:   12-Jan-2018
# @Project: Blueberry
# @Filename: fabfile.py
# @Last modified by:   michael
# @Last modified time: 09-Feb-2021
# @License: GNU GPL v3

from __future__ import with_statement

from datetime import datetime, timedelta, timezone

from fabric import task
from invocations.console import confirm
from invoke import Exit

import config as cfg
import src.api.BDD as bdd
from src.plugins.carto.Ip import Ip

my_hosts = cfg.hosts


@task
def prepare_data_test(c):
    """Creer les data nécéssaires aux tests."""
    offset = timezone(timedelta(hours=2))
    date = datetime.now(offset).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    c.run("sed 's/{DATE}/" + date +
          "/g' src/test/data/suricata-log.temp.json > src/test/data/suricata-log.json")


@task
def test(c):
    """Lance test unitaire."""
    prepare_data_test(c)
    result = c.run(
        "./venv/bin/python3 -m pytest", warn=True)



@task
def test_code(c):
    """Lance code security analyse."""
    result = c.run("./venv/bin/bandit -r ./ -x *config.py,*test*.py", warn=True)



@task
def install(c):
    """Install blueberry."""
    config_service(c)
    config_bdd()
    c.run("mkdir log")
    c.run("touch log/blueberry.log")


@task
def config_service(c):
    """Configure le service Blueberry."""
    c.run(
        "sed -e \"s/{{{{dir}}}}/{}/g\" install/blueberry.service >> /etc/systemd/system/blueberry.service".format(
            cfg.work_dir.replace("/", "\/")))
    c.run("chown root: /etc/systemd/system/blueberry.service", warn=True)


def config_bdd():
    """Permet l'installation de la BDD automatise."""
    try:
        var = bdd.db.connect
        bdd.db.create_tables([Ip])
    except Exception as e:
        print("=== La base SQL existe déjà ===")
        print(e)


@task(hosts=my_hosts)
def uninstall(c):
    c.run("systemctl stop blueberry")
    c.run("rm /etc/systemd/system/blueberry.service")


@task
def commit(c):
    """Git commit."""
    c.run("git commit")


@task
def push(c):
    """Git push."""
    c.run("git push")


@task
def prepare_deploy(c):
    """Test + commit + push."""
    test(c)
    test_code(c)
    commit(c)
    push(c)


@task(hosts=my_hosts)
def deploy(c):
    """Deploy sur le serveur."""
    # prepare_deploy()
    code_dir = cfg.hosts_dir
    command = "sudo sh -c 'cd {} && git pull'".format(code_dir)
    command2 = "chown -R blueberry: {}".format(code_dir)
    c.run(command, pty=True)
    c.run(command2, pty=True)
    c.run('sudo systemctl restart blueberry', warn=True, pty=True)


@task(hosts=my_hosts)
def stop_server(c):
    """Stop le serveur."""
    c.run("sudo systemctl stop blueberry", warn=True, pty=True)


@task
def start_local(c):
    """Demarre en local."""
    commande = "./venv/bin/python3 main.py"
    c.run(commande, pty=True)


@task(hosts=my_hosts)
def start_server(c):
    """Start le serveur."""
    c.run('sudo systemctl start blueberry', warn=True, pty=True)
