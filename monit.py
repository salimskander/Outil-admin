import psutil
import json
import os
import datetime
import socket
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.getcwd()
MONIT_DIR = os.path.join(BASE_DIR, "monit")
CONFIG_FILE_PATH = os.path.join(BASE_DIR,  "conf", "monit_config.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def setup_logging():
    if not os.path.exists(MONIT_DIR):
        os.makedirs(MONIT_DIR)

    log_file = os.path.join(MONIT_DIR, "monit.log")

    logger = logging.getLogger("monit_logger")
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(log_file, maxBytes=102400, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)

    monit_file_handler = RotatingFileHandler(os.path.join(MONIT_DIR, "monit.log"), maxBytes=102400, backupCount=5)
    monit_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(monit_file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

setup_logging()

def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        return {}

    with open(CONFIG_FILE_PATH, "r") as config_file:
        return json.load(config_file)

def save_config(config):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(config, config_file, indent=2)

def check_resources():
    cpu_percent = psutil.cpu_percent()
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

    report_file = os.path.join(REPORTS_DIR, f"report_{report['id']}.json")
    with open(report_file, "w") as report_file:
        json.dump(report, report_file, indent=2)

    logging.info("Check completed and report generated.")
    return report


def list_reports():
    if not os.path.exists(REPORTS_DIR):
        logging.warning("Reports directory doesn't exist.")
        return []

    reports = [f for f in os.listdir(REPORTS_DIR) if f.startswith("report_")]
    logging.info("List of available reports: %s", reports)
    print(reports)
    return reports

import os

def get_last_report():
    reports = list_reports()
    if reports:

        reports_with_dates = [(report, os.path.getctime(os.path.join(REPORTS_DIR, report))) for report in reports]
        sorted_reports = sorted(reports_with_dates, key=lambda x: x[1], reverse=True)
        latest_report_name = sorted_reports[0][0]
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
    recent_reports = sorted(reports, reverse=True)[:last_x_hours]

    if recent_reports:
        average_report = {"cpu_percent": 0, "ram_percent": 0, "disk_percent": 0}

        for report_id in recent_reports:
            report_file = os.path.join(REPORTS_DIR, report_id)
            with open(report_file, "r") as report_file:
                report_data = json.load(report_file)

            average_report["cpu_percent"] += report_data["cpu_percent"]
            average_report["ram_percent"] += report_data["ram_percent"]
            average_report["disk_percent"] += report_data["disk_percent"]

        total_reports = len(recent_reports)
        average_report["cpu_percent"] /= total_reports
        average_report["ram_percent"] /= total_reports
        average_report["disk_percent"] /= total_reports

        logging.info(
            "Calculated the average report for the last %d hours.", last_x_hours
        )
        return average_report
    else:
        logging.warning("No reports available.")
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
    
    if "check" in os.sys.argv:
        check_resources()

    elif "list" in os.sys.argv:
        list_reports()

    elif "get" in os.sys.argv and "last" in os.sys.argv:
        get_last_report()

    elif "get" in os.sys.argv and "avg" in os.sys.argv and len(os.sys.argv) == 4:
        last_x_hours = int(os.sys.argv[3])
        get_average_report(last_x_hours)

    else:
        print("Usage: python monit.py [check | list | get last | get avg X]")

