# Blueberry

## Description

Cet outil permet superviser une sonde réseaux ainsi d'un ensemble d'autre outils de sécurité, dont:
- Suricata (NIDS)
- logwatch


  Cet outil peut donc être considéré comme intrusif. Vérifié que vous avez bien l'accord de votre administrateur réseaux avant de déployer cet outil.

## Commandes disponibles

`\help` permet d'afficher les commandes disponibles


| Commande | Description |
| ------ | --- |
| `\nids` | Permet de savoir si le job est activé. Lorsque c'est le cas, le script vérifie toutes les heures (fréquence configurable via config.py) si suricata a levé une alerte. |
| `\sysinfo` | Donne l'état de la machine. |
| `\log` | Affiche les logs de Blueberry. Permet aussi de les supprimer. |
| `\help` | Affiche l'aide. |


## Installation

*Vous n'avez rien a faire si vous utilisez le script d'installation [Blueberry-Ansible](https://gitlab.com/mic-rigaud/blueberry-ansible)*

Tout d'abord il faut copier config.py.exemple en config.py

```
cp config.py.exemple config.py
```

Puis il faut compléter le fichier de configuration

```
nano config.py
```

Enfin:
```shell
pip3 install -r requirements.txt
fab install
fab start_local
```


## FAQ

### Pourquoi ce nom?

Ce nom a été choisi pour deux raisons:
- Premièrement, Blueberry a pour but d'être installé sur un raspberry. Et les gâteau aux myrtilles et aux framboises sont les meilleurs!
- Deuxièmement, ce logiciel doit chasser les intrus sur notre réseau. On peut voir le parallèle avec la BD de cow-boy de même nom... On va chasser les méchants!
