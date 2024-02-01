import os
import json
import datetime
import socket
import logging
from logging.handlers import RotatingFileHandler
import psutil

# Configurations
LOG_DIR = "/var/monit"
REPORTS_DIR = "/var/monit/reports"


class Monitor:
    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        log_file = os.path.join(LOG_DIR, "monit.log")

        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        logging.basicConfig(
            handlers=[RotatingFileHandler(log_file, maxBytes=102400, backupCount=5)],
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )

    def check_resources(self):
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage("/").percent

        ports_to_monitor = [80, 443]  # Example ports to monitor

        # Check Ports
        ports_status = {}
        for port in ports_to_monitor:
            ports_status[port] = self.is_port_open("127.0.0.1", port)

        report = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": str(hash(datetime.datetime.now())),
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "disk_percent": disk_percent,
            "ports_status": ports_status,
        }

        report_file = os.path.join(REPORTS_DIR, f"report_{report['id']}.json")
        with open(report_file, "w") as report_file:
            json.dump(report, report_file, indent=2)

        logging.info("Check completed and report generated.")
        return report

    def is_port_open(self, host, port):
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False


if __name__ == "__main__":
    monitor = Monitor()

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    # Command
    if "check" in os.sys.argv:
        report = monitor.check_resources()
        print("Report generated:\n")
        print(f"id : {report['id']}")
        print(f"timestamp : {report['timestamp']}")
        print(f"cpu_percent : {str(report['cpu_percent'])}%")
        print(f"ram_percent : {str(report['ram_percent'])}%")
        print(f"disk_percent : {str(report['disk_percent'])}%")
        print(f"ports_status : {str(report['ports_status'])}")

    else:
        print("Usage: python monit.py [check]")
