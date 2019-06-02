# Blueberry

## Description

Cet outil doit être un outil pour superviser de la sécurité d'un réseau personnel. Il doit permettre notamment de:
- donner un aperçu de l'ensemble des machines présentes sur le réseaux;
- donner des fiches à appliquer;
- proposer des sites pour renforcer votre sécurité;
- proposer des analyses de votre réseaux pour en déterminer le niveau de sécurité global;

Cet outil utilisera les outils suivants sur votre réseaux:

- ping
- nmap
- arp

  Cet outil peut donc être considéré comme intrusif. Vérifié que vous avez bien l'accord de votre administrateur réseaux avant de déployer cet outil.

## Suivi de versions

Nous en sommes à la **version 0.1**.

### Objectifs pour la **version 1.0**:

- Analyser le réseau pour détecter toutes les machines présentes
- Enregistrer les machines présentes avec leur MAC et leur nom DNS
- Disposer d'une interface graphique permettant de lister les machines présentes, et de proposer d'autres outils

### Objectifs pour la **version 2.0**:

- Analyse du réseau et détection des vulnérabilités critiques
- Cartographie du réseaux sous format graphique

### Objectifs pour la **version 3.0**:

- Analyser à la demande les machines sur le réseaux pour en connaître leur vulnérabilités
- Envoyer ce Bilan à l'administrateur du réseaux

## FAQ

### Pourquoi ce nom?

Ce nom a été choisi pour deux raisons:
- Premièrement, Blueberry à pour but d'être installé sur un raspberry. Et les gâteau aux myrtilles et aux framboises sont les meilleurs!
- Deuxièmement, ce logiciel doit chasser les intrus sur notre réseau. On peut voir le parallèle avec la BD de cow-boy de même nom... On va chasser les méchants!
