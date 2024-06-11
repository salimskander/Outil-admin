from flask import Flask, render_template, jsonify
from monit import check_resources, list_reports, get_last_report, get_average_report

app = Flask(__name__)

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
    app.run(debug=True)
