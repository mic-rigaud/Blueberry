# @Author: michael
# @Date:   12-Jan-2018
# @Project: Blueberry
# @Filename: fabfile.py
# @Last modified by:   michael
# @Last modified time: 26-Jun-2019
# @License: GNU GPL v3

from __future__ import with_statement

import config as cfg
from fabric.api import abort, cd, env, local, run, settings
from fabric.contrib.console import confirm

env.hosts = cfg.hosts


# TODO: Il va falloir penser au package mock
def test():
    """Lance test unitaire."""
    with settings(warn_only=True):
        result = local('py.test', capture=True)
    print(result)
    if result.failed and not confirm("Les tests ont échoué. On continue?"):
        abort("Annulation sur demande utilisateur.")


def install():
    """Install blueberry."""
    copy_config()
    config_service()
    config_ossec()
    config_zeek()


def copy_config():
    """Copy le fichier de config a cote du main."""
    # TODO: Test que le fichier de config est propre
    local("cp config.py blueberry/config.py")


def config_service():
    """Configure le service Blueberry."""
    local(
        "sed -e \"s/{{dir}}/{}/g\" install/blueberry.service >> /etc/systemd/system/blueberry.service".format(cfg.dir))
    local("chown root: /etc/systemd/system/blueberry.service")
    local("systemctl enable blueberry.service")


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


def commit():
    """Git commit."""
    local("git commit")


def push():
    """Git push."""
    local("git push")


def prepare_deploy():
    """Test + commit + push."""
    test()
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
    cmd = "rm " + cfg.log
    local(cmd)
    code_dir = cfg.dir
    with cd(code_dir):
        run(cmd)


def start_local(args=""):
    """Demarre en local."""
    commande = "python3 blueberry/main.py" + args
    local(commande)
