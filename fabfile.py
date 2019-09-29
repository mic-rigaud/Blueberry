# @Author: michael
# @Date:   12-Jan-2018
# @Project: Blueberry
# @Filename: fabfile.py
# @Last modified by:   michael
# @Last modified time: 29-Sep-2019
# @License: GNU GPL v3

from __future__ import with_statement

from datetime import datetime, timedelta, timezone

import config as cfg
from fabric.api import abort, env, local, run, settings
from fabric.context_managers import cd, lcd
from fabric.contrib.console import confirm

import blueberrycore.api.api_bdd as bdd

env.hosts = cfg.hosts


def prepare_data_test():
    """Creer les data nécéssaires aux tests."""
    offset = timezone(timedelta(hours=2))
    date = datetime.now(offset).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    local("sed 's/{DATE}/" + date +
          "/g' blueberryui/tests/data/suricata-log.temp.json > blueberryui/tests/data/suricata-log.json")


def test():
    """Lance test unitaire."""
    prepare_data_test()
    with lcd("./blueberryui"):
        with settings(warn_only=True):
            result = local('python -m pytest --cov=. tests', capture=True)
            print(result)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def test_code():
    """Lance code security analyse."""
    with settings(warn_only=True):
        result = local('bandit -r ./ -x *config.py', capture=True)
    print(result)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def install():
    """Install blueberry."""
    copy_config()
    config_service()
    config_ossec()
    config_zeek()


def copy_config():
    """Copy le fichier de config a cote du main."""
    # TODO: Test que le fichier de config est propre
    local("cp config.py blueberryui/config.py")
    local("cp config.py blueberrycore/config.py")


def config_service():
    """Configure le service Blueberry."""
    local(
        "sed -e \"s/{{{{dir}}}}/{}/g\" install/blueberry.service >> /etc/systemd/system/blueberry.service".format(cfg.dir.replace("/", "\/")))
    local("chown root: /etc/systemd/system/blueberry.service")
    # Permet d'éviter de planter dans les runner Gitlab-CI
    with settings(warn_only=True):
        result = local("systemctl enable blueberry.service")


def config_ossec():
    """Install Bluebrry for Ossec."""
    # TODO: Verifier que ossec est bien présent
    local("cp install/sendEvent.sh /var/ossec/active-response/bin/")
    local(
        "sed -i \"s/{{token}}/{}/g\" /var/ossec/active-response/bin/sendEvent.sh".format(cfg.ossec_token))
    local(
        "sed -i \"s/{{chat_id}}/{}/g\" /var/ossec/active-response/bin/sendEvent.sh".format(cfg.chat_id))
    local("chown root:ossec /var/ossec/active-response/bin/sendEvent.sh")
    local("chmod 750 /var/ossec/active-response/bin/sendEvent.sh")
    # TODO: rajouter la partie command dans ossec.conf
    local("systemctl restart ossec")


def config_zeek():
    pass


def config_bdd():
    """Permet l'installation de la BDD automatise."""
    try:
        bdd.db.connect
        bdd.db.create_tables([bdd.Ip])
    except:
        print("=== La base SQL existe déjà ===")


def uninstall():
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
    prepare_deploy()
    code_dir = cfg.dir
    with cd(code_dir):
        run('git pull')
        run('systemctl restart blueberry')


def stop_server():
    """Stop le serveur."""
    run('systemctl stop blueberry')


def clean():
    """Netoie les logs."""
    local("rm log/blueberry.log")
    cmd = "rm " + cfg.log
    code_dir = cfg.dir
    with cd(code_dir):
        run(cmd)


def start_local(args=""):
    """Demarre en local."""
    commande = "python3 blueberryui/main.py" + args
    local(commande)
