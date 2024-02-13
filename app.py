from flask import Flask, render_template, jsonify
from monit import check_resources, list_reports, get_last_report, get_average_report
import time
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1206600943270109194/lq9kpm50CJXFLGbepJfrbjNBW5_thkAdLI7jwjeFewrehpWJL8S0412--6Lwj9JEfccL"

def send_discord_notification(message):
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def monitor_resources():
    while True:
        report = check_resources()
        if report["ram_percent"] > 40.5:
            message = f"Attention: Utilisation de la RAM au-dessus de 40,5%! RAM utilisée: {report['ram_percent']}%"
            send_discord_notification(message)
        time.sleep(10)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/check")
def api_check():
    return jsonify(check_resources())


@app.route("/api/list_reports")
def api_list_reports():
    return jsonify(list_reports())


@app.route("/api/get_last_report")
def api_get_last_report():
    return jsonify(get_last_report())


@app.route("/api/get_average_report/<int:last_x_hours>")
def api_get_average_report(last_x_hours):
    return jsonify(get_average_report(last_x_hours))

if __name__ == "__main__":
    # Démarrer le thread de surveillance en arrière-plan
    import threading
    monitor_thread = threading.Thread(target=monitor_resources)
    monitor_thread.start()


