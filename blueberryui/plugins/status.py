
"""Affiche le status de la raspberry."""
import psutil
import telegram
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from api.Restricted import restricted


def status_suricata():
    """Retourne le status de suricata."""
    reponse = "☠️"
    for proc in psutil.process_iter(attrs=['pid', 'name', 'status']):
        if "suricata" in proc.info["name"].lower():
            reponse = "✅"
    return reponse


def status_cpu():
    """Retourne le status de suricata."""
    cpu_percent = psutil.cpu_percent()
    return str(cpu_percent)


def status_ram():
    ram = psutil.virtual_memory()
    return str(ram.percent)


def temperature_raspberry():
    temp = psutil.sensors_temperatures()
    if 'cpu-thermal' in temp:
        return temp['cpu-thermal'][0].current
    return "0"


def status_str():
    reponse = "Les infos de votre raspberry:\n"
    reponse += "<b>Temperature:</b> " + temperature_raspberry() + "°C\n"
    reponse += "<b>CPU:</b> " + status_ram() + "%\n"
    reponse += "<b>RAM:</b> " + status_cpu() + "%\n"
    reponse += "<b>Suricata:</b> " + status_suricata() + "\n"
    return reponse


@restricted
def status(update: Update, context: CallbackContext):
    """Affiche le status de la raspberry."""
    reponse = status_str()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=reponse,
                             parse_mode=telegram.ParseMode.HTML)


def add(dispatcher):
    """
    Affiche le status de la raspberry.
    """
    handler = CommandHandler('status', status)
    dispatcher.add_handler(handler)
