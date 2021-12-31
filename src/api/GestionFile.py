# @Author: michael
# @Date:   17-Jun-2018
# @Filename: GestionFile.py
# @Last modified by:   michael
# @Last modified time: 07-Aug-2018
# @License: GNU GPL v3

import json
import logging


def file_ajouter(file, key, values):
    """Ajout un element json dans un fichier."""
    contenu = {}
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
    except FileNotFoundError:
        logging.info("Le fichier n'existe pas. Il va etre cree")
    if key in contenu:
        logging.warning("L'élément {0} est deja présent".format(key))
        return "<i>L'élément est déjà présent</i>"
    values["id"] = len(contenu) + 1
    contenu[key] = values
    with open(file, "w") as fichier:
        fichier.write(json.dumps(contenu, indent=4))
    return "<i>Elément ajouté avec succes</i>"


def file_supprimer(file, id):
    """Supprime un element dans un fichier."""
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        contenu2 = dict(contenu)
        for element in contenu:
            if int(id) == int(contenu[element]["id"]):
                contenu2.pop(element)
            elif int(id) < int(contenu[element]["id"]):
                contenu2[element]["id"] = int(contenu[element]["id"]) - 1
        with open(file, "w") as fichier:
            fichier.write(json.dumps(contenu2, indent=4))
        return "Effacement avec succes"
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        return "<i>Fichier inexistant</i>"
    except ValueError as e:
        logging.error("Entre n est pas un int: {}".format(e))
        return "<b>Veuiller entrer un int</b>"


def file_liste(file):
    """Lister les éléments d'un fichier."""
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        contenu_sorted = sorted(contenu.items(), key=lambda t: t[1]["id"])
        if contenu_sorted == "":
            logging.warning("Aucun element dans le fichier {0}".format(file))
            raise Exception("fichier vide")
        return contenu_sorted
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        raise FileNotFoundError


def file_get(file, id):
    """Recuperer un element a partir de l id."""
    try:
        with open(file, "r") as f:
            contenu = json.load(f)
        if contenu == "":
            logging.warning("Aucun element dans le fichier {0}".format(file))
            raise Exception("fichier vide")
        for element in contenu:
            if int(id) == contenu[element]["id"]:
                return element, contenu[element]
        logging.warning("ID invalide. Fourni: {0}".format(id))
        raise Exception("l'id n est pas présent")
    except FileNotFoundError:
        logging.warning("Le fichier n'existe pas.")
        raise FileNotFoundError("Le fichier n'existe pas")
    except ValueError as e:
        logging.error("Entre n est pas un int: {}".format(e))
        raise ValueError("<b>Veuiller entrer un int</b>")
