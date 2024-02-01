import psutil
import json
import argparse

def get_system_info():
    # Obtient les informations sur l'utilisation du CPU, de la RAM et du disque
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    # Vous pouvez ajouter d'autres informations comme la température du CPU, la charge système, etc.

    # Crée un dictionnaire avec les informations collectées
    system_info = {
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage
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

    # Vous pouvez ajouter d'autres formats de sortie selon vos besoins

if __name__ == "__main__":
    main()
