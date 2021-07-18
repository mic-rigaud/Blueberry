import psutil

MAX_DISQUE = 85
MAX_TEMPERATURE = 80


def status_service(service):
    """Retourne le status de suricata."""
    reponse = "☠️"
    for proc in psutil.process_iter(attrs=['pid', 'name', 'status']):
        if service in proc.info["name"].lower():
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
    if 'coretemp' in temp:
        return str(temp['coretemp'][0].current)
    return "0"


def status_disk():
    """Affiche le pourcentage d'utilisation du disque"""
    disk = psutil.disk_usage('/')
    return str(disk.percent)


def sysinfo_job():
    """sysinfo_job: verifie que le disque n'est pas plein et verifie que la temperatures est correct"""
    reponse = ""
    if float(status_disk()) > MAX_DISQUE:
        reponse += "Attention, vous avez dépassé les {}% d'utilisation du disque\n".format(MAX_DISQUE)
    temp = psutil.sensors_temperatures()
    if 'coretemp' in temp:
        current = temp['coretemp'][0].current
        critical = temp['coretemp'][0].critical
        pourcent = (current / critical) * 100
        if pourcent > MAX_TEMPERATURE:
            reponse += "Attention, votre serveur à chaud. Il a dépassé les {}% de température\n".format(MAX_TEMPERATURE)
    return reponse


def status_str():
    reponse = "Les infos de votre raspberry:\n"
    reponse += "<b>Temperature:</b> " + temperature_raspberry() + "°C\n"
    reponse += "<b>CPU:</b> " + status_ram() + "%\n"
    reponse += "<b>RAM:</b> " + status_cpu() + "%\n"
    reponse += "<b>Usage Disk:</b> " + status_disk() + "%\n"
    reponse += "<b>Suricata:</b> " + status_service("suricata") + "\n"
    reponse += "<b>Arpwatch:</b> " + status_service("arpwatch") + "\n"
    return reponse
