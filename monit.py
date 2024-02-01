import psutil
import json
import argparse
import platform

def get_system_info():
    # Obtient les informations sur l'utilisation du CPU, de la RAM et du disque
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Obtient des informations sur le CPU, y compris la température si disponible
    cpu_info = {}
    try:
        # Surveiller la température du CPU (peut varier en fonction du matériel)
        temps = psutil.sensors_temperatures()
        cpu_temp = temps['coretemp'][0].current if 'coretemp' in temps else None
        cpu_info['temperature'] = cpu_temp
    except Exception as e:
        cpu_info['temperature'] = None

    # Obtient la charge système moyenne sur 1, 5 et 15 minutes
    system_load = psutil.getloadavg()

    # Crée un dictionnaire avec les informations collectées
    system_info = {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
        "cpu_info": cpu_info,
        "system_load": {
            "load_1min": system_load[0],
            "load_5min": system_load[1],
            "load_15min": system_load[2]
        },
        "system_platform": platform.system(),
        "system_version": platform.version()
        # Ajoutez d'autres clés et valeurs selon vos besoins
    }

    return system_info

def main():
    # Initialise l'analyseur d'arguments de la ligne de commande
    parser = argparse.ArgumentParser(description='Outil de monitoring système')
    parser.add_argument('--json', action='store_true', help='Retourne les résultats au format JSON')

    # Analyse les arguments de la ligne de commande
    args = parser.parse_args()

    # Obtient les informations système
    system_info = get_system_info()

    # Si l'option --json est spécifiée, imprime les résultats au format JSON
    if args.json:
        print(json.dumps(system_info, indent=2))
    else:
        # Sinon, imprime les résultats de manière lisible
        print("Utilisation CPU: {}%".format(system_info["cpu_usage"]))
        print("Utilisation RAM: {}%".format(system_info["ram_usage"]))
        print("Utilisation du disque: {}%".format(system_info["disk_usage"]))

        # Informations supplémentaires sur le CPU
        cpu_info = system_info.get("cpu_info", {})
        if cpu_info.get("temperature") is not None:
            print("Température du CPU: {}°C".format(cpu_info["temperature"]))

        # Charge système moyenne
        print("Charge système (1min/5min/15min): {:.2f} {:.2f} {:.2f}".format(
            system_info["system_load"]["load_1min"],
            system_info["system_load"]["load_5min"],
            system_info["system_load"]["load_15min"]
        ))

        # Informations sur la plateforme système
        print("Plateforme système: {}".format(system_info["system_platform"]))
        print("Version du système: {}".format(system_info["system_version"]))

if __name__ == "__main__":
    main()
