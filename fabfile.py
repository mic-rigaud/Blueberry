# @Author: michael
# @Date:   12-Jan-2018
# @Project: Blueberry
# @Filename: fabfile.py
# @Last modified by:   michael
# @Last modified time: 07-Feb-2021
# @License: GNU GPL v3

from __future__ import with_statement

from datetime import datetime, timedelta, timezone

import config as cfg
from fabric.api import abort, env, local, run, settings, sudo
from fabric.context_managers import cd, lcd
from fabric.contrib.console import confirm

import src.api.BDD as bdd
from src.plugins.carto.Ip import Ip

env.hosts = cfg.hosts


def prepare_data_test():
    """Creer les data nécéssaires aux tests."""
    offset = timezone(timedelta(hours=2))
    date = datetime.now(offset).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    local("sed 's/{DATE}/" + date +
          "/g' src/test/data/suricata-log.temp.json > src/test/data/suricata-log.json")


def test():
    """Lance test unitaire."""
    prepare_data_test()
    with lcd("./src"):
        with settings(warn_only=True):
            result = local('python3 -m pytest --cov=. ./', capture=True)
            print(result)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def test_code():
    """Lance code security analyse."""
    with settings(warn_only=True):
        result = local('bandit -r ./ -x *config.py,*test*.py', capture=True)
    print(result)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def install():
    """Install blueberry."""
    copy_config()
    config_service()
    config_bdd()
    local("mkdir log")
    local("touch log/blueberry.log")


def copy_config():
    """Copy le fichier de config a cote du main."""
    # TODO: Test que le fichier de config est propre
    local("cp config.py src/config.py")


def config_service():
    """Configure le service Blueberry."""
    local(
        "sed -e \"s/{{{{dir}}}}/{}/g\" install/blueberry.service >> /etc/systemd/system/blueberry.service".format(cfg.work_dir.replace("/", "\/")))
    local("chown root: /etc/systemd/system/blueberry.service")
    # Permet d'éviter de planter dans les runner Gitlab-CI
    with settings(warn_only=True):
        result = local("systemctl enable blueberry.service")


def config_bdd():
    """Permet l'installation de la BDD automatise."""
    try:
        bdd.db.connect
        bdd.db.create_tables([Ip])
    except:
        print("=== La base SQL existe déjà ===")


def uninstall():
    local("systemctl stop blueberry")
    local("rm /etc/systemd/system/blueberry.service")


def commit():
    """Git commit."""
    local("git commit")


def push():
    """Git push."""
    local("git push")


def prepare_deploy():
    """Test + commit + push."""
    test()
    test_code()
    commit()
    push()


def deploy():
    """Deploy sur le serveur."""
    # prepare_deploy()
    code_dir = cfg.hosts_dir
    with cd(code_dir):
        sudo('git pull')
        sudo('systemctl restart blueberry')


def stop_server():
    """Stop le serveur."""
    code_dir = cfg.hosts_dir
    with cd(code_dir):
        sudo('systemctl stop blueberry')


def start_local(args=""):
    """Demarre en local."""
    commande = "python3 main.py" + args
    local(commande)


def start_server():
    """Start le serveur."""
    code_dir = cfg.hosts_dir
    with cd(code_dir):
        sudo('systemctl start blueberry')
