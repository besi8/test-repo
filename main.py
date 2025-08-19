from flask import Flask, request, jsonify
import os
import zipfile
import io
import requests
from datetime import datetime

app = Flask(__name__)

NETLIFY_TOKEN = os.environ.get("NETLIFY_TOKEN")
NETLIFY_ACCOUNT_ID = os.environ.get("NETLIFY_ACCOUNT_ID")

@app.route("/", methods=["GET"])
def index():
    return "Webhook server is running."

@app.route("/publish", methods=["POST"])
def publish():
    html = request.form.get("html")
    if not html:
        return jsonify({"error": "Missing HTML content"}), 400

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    site_name = f"html-site-{timestamp}"

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("index.html", html)
    zip_buffer.seek(0)

    headers = {
        "Authorization": f"Bearer {NETLIFY_TOKEN}",
    }

    files = {
        "file": ("site.zip", zip_buffer, "application/zip")
    }

    response = requests.post(
        f"https://api.netlify.com/api/v1/sites",
        headers=headers,
        files=files
    )

    if response.status_code == 200 or response.status_code == 201:
        data = response.json()
        return jsonify({
            "site_name": data.get("name"),
            "url": data.get("url"),
            "deploy_url": data.get("deploy_url")
        }), 200
    else:
        return jsonify({
            "error": "Failed to publish to Netlify",
            "details": response.json()
        }), response.status_code
