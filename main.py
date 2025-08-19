from flask import Flask, request, jsonify
import os
import zipfile
import io
import requests
import json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "✅ Aplikacioni është gjallë!"

@app.route("/publish", methods=["POST"])
def publish():
    html_content = request.form.get("html")

    if not html_content:
        return jsonify({"error": "No HTML content provided"}), 400

    # Create ZIP archive in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("index.html", html_content)
    zip_buffer.seek(0)

    # Send to Netlify
    NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
    NETLIFY_SITE_ID = os.getenv("NETLIFY_SITE_ID")

    if not NETLIFY_TOKEN or not NETLIFY_SITE_ID:
        return jsonify({"error": "Missing Netlify credentials"}), 500

    headers = {
        "Authorization": f"Bearer {NETLIFY_TOKEN}"
    }

    files = {
        "file": ("site.zip", zip_buffer, "application/zip")
    }

    response = requests.post(
        f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys",
        headers=headers,
        files=files
    )

    if response.status_code == 200 or response.status_code == 201:
        return jsonify({"message": "Deploy successful", "netlify_url": response.json().get("deploy_ssl_url")})
    else:
        return jsonify({"error": "Deploy failed", "details": response.text}), 500
