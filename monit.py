import psutil
import json
import os
import datetime
import socket
import logging
from logging.handlers import RotatingFileHandler

# Utilisation de chemins spécifiques à Windows
BASE_DIR = os.getcwd()
MONIT_DIR = os.path.join(BASE_DIR, "monit")
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "conf", "monit_config.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def setup_logging():
    if not os.path.exists(MONIT_DIR):
        os.makedirs(MONIT_DIR)

    log_file = os.path.join(MONIT_DIR, "monit.log")

    logger = logging.getLogger("monit_logger")
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(log_file, maxBytes=102400, backupCount=5)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

setup_logging()

def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        return {"ports": []}

    with open(CONFIG_FILE_PATH, "r") as config_file:
        return json.load(config_file)

def save_config(config):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(config, config_file, indent=2)

def check_resources():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage("/").percent

    ports_status = check_ports_status(load_config())

    report = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": str(hash(datetime.datetime.now())),
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "disk_percent": disk_percent,
        "ports_status": ports_status,
    }

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    # Déterminer le nombre de rapports existants et générer le nom du nouveau rapport
    existing_reports = [f for f in os.listdir(REPORTS_DIR) if f.startswith("Report ")]
    report_number = len(existing_reports) + 1
    report_file_name = f"Report {report_number}.json"
    report_file_path = os.path.join(REPORTS_DIR, report_file_name)
    
    with open(report_file_path, "w") as report_file:
        json.dump(report, report_file, indent=2)

    logging.info(f"Check completed and report {report_file_name} generated.")
    return report

def list_reports():
    if not os.path.exists(REPORTS_DIR):
        logging.warning("Reports directory doesn't exist.")
        return []

    reports = sorted([f for f in os.listdir(REPORTS_DIR) if f.startswith("Report ")], key=lambda x: int(x.split()[1].split('.')[0]))
    logging.info("List of available reports: %s", reports)
    return reports

def get_last_report():
    reports = list_reports()
    if reports:
        latest_report_name = reports[-1]
        latest_report_path = os.path.join(REPORTS_DIR, latest_report_name)
        with open(latest_report_path, "r") as report_file:
            last_report = json.load(report_file)
        logging.info("Retrieved the last report.")
        return last_report
    else:
        logging.warning("No reports available.")
        return None

def get_average_report(last_x_hours):
    reports = list_reports()
    if not reports:
        logging.warning("No reports available.")
        return None

    recent_reports = []
    cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=last_x_hours)
    
    for report in reports:
        report_path = os.path.join(REPORTS_DIR, report)
        report_time = datetime.datetime.fromtimestamp(os.path.getctime(report_path))
        if report_time >= cutoff_time:
            with open(report_path, "r") as report_file:
                report_data = json.load(report_file)
                recent_reports.append(report_data)

    if recent_reports:
        average_report = {"cpu_percent": 0, "ram_percent": 0, "disk_percent": 0}
        total_reports = len(recent_reports)

        for report_data in recent_reports:
            average_report["cpu_percent"] += report_data["cpu_percent"]
            average_report["ram_percent"] += report_data["ram_percent"]
            average_report["disk_percent"] += report_data["disk_percent"]

        average_report["cpu_percent"] /= total_reports
        average_report["ram_percent"] /= total_reports
        average_report["disk_percent"] /= total_reports

        logging.info("Calculated the average report for the last %d hours.", last_x_hours)
        return average_report
    else:
        logging.warning("No reports available in the last %d hours.", last_x_hours)
        return None

def is_port_open(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def check_ports_status(config):
    logging.info("Loaded configuration: %s", config)
    ports_status = {}
    for port in config.get("ports", []):
        port_status = "Open" if is_port_open("127.0.0.1", port) else "Closed"
        ports_status[port] = port_status

    logging.info("Port status: %s", ports_status)
    return ports_status

if __name__ == "__main__":
    import sys

    if "check" in sys.argv:
        check_resources()

    elif "list" in sys.argv:
        list_reports()

    elif "get" in sys.argv and "last" in sys.argv:
        print(json.dumps(get_last_report(), indent=2))

    elif "get" in sys.argv and "avg" in sys.argv and len(sys.argv) == 4:
        try:
            last_x_hours = int(sys.argv[3])
            print(json.dumps(get_average_report(last_x_hours), indent=2))
        except ValueError:
            print("Invalid value for X. It should be an integer.")
    else:
        print("Usage: python monit.py [check | list | get last | get avg X]")