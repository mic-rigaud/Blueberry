# Blueberry

## Description

Cet outil permet superviser via Telegram un ensemble d'autre outils de sécurité, dont :
- [suricata](https://suricata-ids.org/) (NIDS)
- [logwatch](https://doc.ubuntu-fr.org/logwatch)
- [arpwatch](https://linux.die.net/man/8/arpwatch)


## Commandes disponibles

`\help` permet d'afficher les commandes disponibles


| Commande | Description |
| ------ | --- |
| `\nids` | Permet de savoir si le job est activé. Lorsque c'est le cas, le script vérifie toutes les heures (fréquence configurable via config.py) si suricata a levé une alerte. Il est également possible de lancer une recherche d'alertes manuellement. |
| `\sysinfo` | Donne l'état de la machine. |
| `\log` | Affiche les logs de Blueberry. Permet aussi de les supprimer. |
| `\logwatch` | Permet d'afficher le rapport [logwatch](https://doc.ubuntu-fr.org/logwatch). Le rapport est également envoyé tous les jours à une heure configurable |
| `\arpwatch` | Permet de lister les machines vu par [arpwatch](https://linux.die.net/man/8/arpwatch) et alerte si une nouvelle machine apparaît. L'alerte est remonté une fois par jours à une heure configurable. |
| `\carto` | Renvoi une cartographie du réseau sous la forme d'un mind map. Attention, cette fonction prend pour hypothèse que votre réseau commence en '192.168' et qu'il n'y a qu'un chemin réseau pour atteindre une machine. Cette cartographie ne fonctionne plus sur des réseaux complexes.|
| `\virustotal` | Permet de scanner une url via l'api de [virustotal](https://www.virustotal.com/) |
| `\whois` | Permet de faire un whois sur une adresse ip/url/domaine. Les informations sont récupérées sur  [whois xml API](https://www.whoisxmlapi.com) |
| `\observatory` | Permet d'évaluer une nom de domaine au niveau `http` et `tls` avec les outils de [Mozilla](https://observatory.mozilla.org/) |
| `\scan` | Lance un scan de l'URL ou Domain ou IP en utilisant les plugins installés par ailleurs |
| `\help` | Affiche l'aide. |


## Installation

*Vous n'avez rien a faire si vous utilisez le script d'installation [Blueberry-Ansible](https://gitlab.com/mic-rigaud/blueberry-ansible)*

Tout d'abord il faut copier config.test en config.py

```
cp test/install/config.test config.py
```

Puis il faut compléter le fichier de configuration

```
nano config.py
```

Enfin:
```shell
pip3 install -r requirements.txt
fab install
systemctl start blueberry
```


## FAQ

### Pourquoi ce nom?

Ce nom a été choisi pour deux raisons:
- Premièrement, Blueberry a pour but d'être installé sur un raspberry. Et les gâteau aux myrtilles et aux framboises sont les meilleurs!
- Deuxièmement, ce logiciel doit chasser les intrus sur notre réseau. On peut voir le parallèle avec la BD de cow-boy de même nom... On va chasser les méchants!

### Pourquoi utiliser Telegram?

Mon besoin est de monitorer un certain nombre d'outil et de réaliser des actions prédéfinies sur demande. De plus, je souhaite être prévenu assez rapidement d'une alerte. Pour cela il n'existe pas pléthore de solution:
- Email - C'est asynchrone. C'est donc bien pour remonter de l'information moins pour faire des requêtes.
- Interface web - L'interface web c'est bien. Mais cela a deux défaut, le premier c'est que pour obtenir les alertes il faut être connecté sur l'appli web ce qui n'est pas évident au quotidien. Le second c'est que si on souhaite avoir accès au portail depuis l’extérieur de son réseau on augmente les risques de sécurité.
- Un appli téléphone - La solution serait parfaite mais longue à développer. De plus, pour que ce soit intéressant il faudrait être compatible MAC - Android - etc...  

Telegram répond donc très bien à mon besoin. Le seul défaut est qu'on ne sait pas comment sont utiliser les données. Pour la sécurité d'un réseau domestique cela ne me pose pas de problèmes.
