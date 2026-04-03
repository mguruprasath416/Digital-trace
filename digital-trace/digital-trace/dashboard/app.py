# dashboard/app.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
from core.username_checker import check_username
from core.dork_generator import generate_dorks
from modules.whois_lookup import whois_lookup
from modules.ipinfo_lookup import ip_lookup
from modules.haveibeenpwned import check_email_breach
from core.report_builder import build_report
from utils.validator import sanitize_input
from config.settings import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, DASHBOARD_USERNAME, DASHBOARD_PASSWORD

app = Flask(__name__, template_folder="templates")
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == DASHBOARD_USERNAME and password == DASHBOARD_PASSWORD

@app.route("/")
@auth.login_required
def index():
    return render_template("index.html")

@app.route("/api/username", methods=["POST"])
@auth.login_required
def api_username():
    data = request.json
    username = sanitize_input(data.get("username", ""))
    if not username:
        return jsonify({"error": "Username required"}), 400
    results = check_username(username)
    return jsonify(results)

@app.route("/api/whois", methods=["POST"])
@auth.login_required
def api_whois():
    data = request.json
    domain = sanitize_input(data.get("domain", ""))
    return jsonify(whois_lookup(domain))

@app.route("/api/ip", methods=["POST"])
@auth.login_required
def api_ip():
    data = request.json
    ip = sanitize_input(data.get("ip", ""))
    return jsonify(ip_lookup(ip))

@app.route("/api/breach", methods=["POST"])
@auth.login_required
def api_breach():
    data = request.json
    email = sanitize_input(data.get("email", ""))
    return jsonify(check_email_breach(email))

@app.route("/api/dorks", methods=["POST"])
@auth.login_required
def api_dorks():
    data = request.json
    target = sanitize_input(data.get("target", ""))
    return jsonify(generate_dorks(target))

@app.route("/api/report", methods=["POST"])
@auth.login_required
def api_report():
    data = request.json
    target = sanitize_input(data.get("target", "unknown"))
    findings = data.get("findings", {})
    path = build_report(target, findings)
    return jsonify({"report_path": path})

if __name__ == "__main__":
    print("\n🔍 DigitalTrace Dashboard starting...")
    print(f"   Open: http://{FLASK_HOST}:{FLASK_PORT}\n")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
```

---

