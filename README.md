# Blueberry

![Gitlab](https://gitlab.com/mic-rigaud/Blueberry/badges/master/pipeline.svg)
![CodeQL](https://github.com/mic-rigaud/Blueberry/workflows/CodeQL/badge.svg?branch=master)

## Description

Cet outil permet superviser via Telegram un ensemble d'autre outils de sécurité, dont :

- [suricata](https://suricata-ids.org/) (NIDS)
- [logwatch](https://doc.ubuntu-fr.org/logwatch)
- [arpwatch](https://linux.die.net/man/8/arpwatch)

![capture-telegram](https://raw.githubusercontent.com/mic-rigaud/Blueberry/master/ressources/capture-telegram.png)

## Commandes disponibles

`\help` permet d'afficher les commandes disponibles

| Commande | Description |
| ------ | --- |
| `\arpwatch` | Permet de lister les machines vu par [arpwatch](https://linux.die.net/man/8/arpwatch) et alerte si une nouvelle machine apparaît. L'alerte est immédiate si arpwatch est configuré pour executer le script ./bin/bluebberry_sendTask.py, sinon l'alerte est remonté après une durée paramétrable. |
| `\carto` | Permet d'avoir la cartographie de votre réseau. Peut réaliser une cartographie sous la forme d'un mind map. Attention, cette fonction graphique prend pour hypothèse que votre réseau commence en '192.168' et qu'il n'y a qu'un chemin réseau pour atteindre une machine. Cette cartographie ne fonctionne plus sur des réseaux complexes.|
| `\log` | Affiche les logs de Blueberry. Permet aussi de les supprimer. |
| `\logwatch` | Permet d'afficher le rapport [logwatch](https://doc.ubuntu-fr.org/logwatch). Le rapport est également envoyé tous les jours à une heure configurable |
| `\nids` | Permet de savoir si le job est activé. Lorsque le job est lancé, blueberry vérifie toutes les heures si suricata a levé une nouvelle alerte. Si c'est le cas, il transmet l'alerte. |
| `\scan` | Lance un scan d'une URL ou d'un Domain ou d'une IP ou d'un numéro de Téléphone en utilisant les plugins installés par ailleurs |
| `\sysinfo` | Donne l'état de la machine. |
| `\virustotal` | Permet de scanner une url via l'api de [virustotal](https://www.virustotal.com/) |
| `\whois` | Permet de faire un whois sur une adresse ip/url/domaine. Les informations sont récupérées sur  [whois xml API](https://www.whoisxmlapi.com) |
| `\help` | Affiche l'aide. |

## Fonctionnalités disponibles

### Surveillance du réseau

Suricata est un NIDS (Network Intrusion Detection System) il permet de détecter les tentatives d'attaques sur le réseau.
Blueberry envoi automatiquement a une fréquence choisi dans *config.py* les alertes remontées par suricata.

Blueberry permet également de voir les modules chargés par Suricata (en dev)

### Detection des nouveaux appareils

Arpwatch est un outil qui permet de détecter les nouvelles machines sur le réseau via les requètes ARP. Blueberry,
informe immédiatement des nouveaux appareils trouvés par arpwatch.

De plus, Blueberry permet de leur donner un Alias via `/carto --> Lister --> [nom de la machine] --> Modifier`

### Scan à la demande

Blueberry s'appuit sur des interfaces web pour proposer des scans sur les objets suivants:

- IP
- Nom de Domain
- URL
- Numéro de téléphone

Les informations renvoyées dépendent de l'objet scanné.

### Etat de la machine

Blueberry permet d'effectuer une supervision de votre machine et vous alerte en cas de problème (température trop haute,
etc...)

## Installation

### Automatisé

Vous pouvez utiliser le script ansible disponible
sur [Blueberry-Ansible](https://gitlab.com/mic-rigaud/blueberry-ansible)

Dans ce cas, suivre uniquement le guide d'utilisation présent sur dépot Ansible.

### Manuelle

*Attention, via cette installation certaines fonctions ne marcherons pas. Par exemple, la détection des nouveaux
appareils ne sera pas temps réel car une modification des script arpwatch est nécessaire.*

Sinon il faut compléter le fichier de configuration

```
nano config.py
```

Enfin:

```shell
pip3 install -r requirements.txt
fab install
systemctl daemon-reload
systemctl start blueberry
```

## FAQ

### Pourquoi ce nom?

Ce nom a été choisi pour deux raisons:

- Premièrement, Blueberry a pour but d'être installé sur un raspberry. Et les gâteaux aux myrtilles et aux framboises
  sont les meilleurs!
- Deuxièmement, ce logiciel doit chasser les intrus sur notre réseau. On peut voir le parallèle avec la BD de cow-boy de
  même nom... On va chasser les méchants!

### Pourquoi utiliser Telegram?

Mon besoin est de monitorer un certain nombre d'outil et de réaliser des actions prédéfinies sur demande. De plus, je
souhaite être prévenu assez rapidement d'une alerte. Pour cela il n'existe pas pléthore de solution:

- Email - C'est asynchrone. C'est donc bien pour remonter de l'information moins pour faire des requêtes.
- Interface web - L'interface web c'est bien. Mais cela a deux défaut, le premier c'est que pour obtenir les alertes il
  faut être connecté sur l'appli web ce qui n'est pas évident au quotidien. Le second c'est que si on souhaite avoir
  accès au portail depuis l’extérieur de son réseau on augmente les risques de sécurité.
- Un appli téléphone - La solution serait parfaite mais longue à développer. De plus, pour que ce soit intéressant il
  faudrait être compatible MAC - Android - etc...

Telegram répond donc très bien à mon besoin. Le seul défaut est qu'on ne sait pas comment sont utiliser les données.
Pour la sécurité d'un réseau domestique cela ne me pose pas de problèmes.
