from flask import Flask, request, jsonify
import zipfile
import os
import uuid
import requests

app = Flask(__name__)

NETLIFY_TOKEN = "your-netlify-access-token"  # Zëvendësoje me token tënd real
NETLIFY_SITE_NAME = "your-site-name"         # P.sh. besi-site-test (pa .netlify.app)
DEPLOY_FOLDER = "deployments"

@app.route("/")
def index():
    return "Server is running."

@app.route("/publish", methods=["POST"])
def publish():
    html = request.form.get("html")
    if not html:
        return jsonify({"error": "Missing 'html' field"}), 400

    os.makedirs(DEPLOY_FOLDER, exist_ok=True)
    unique_id = str(uuid.uuid4())
    folder_path = os.path.join(DEPLOY_FOLDER, unique_id)
    os.makedirs(folder_path, exist_ok=True)

    html_file_path = os.path.join(folder_path, "index.html")
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html)

    zip_path = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(html_file_path, arcname="index.html")

    with open(zip_path, "rb") as f:
        headers = {
            "Authorization": f"Bearer {NETLIFY_TOKEN}",
        }
        response = requests.post(
            f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_NAME}/deploys",
            headers=headers,
            files={"file": ("site.zip", f, "application/zip")},
        )

    if response.status_code == 200:
        netlify_url = response.json().get("deploy_ssl_url")
        return jsonify({"message": "Published successfully", "url": netlify_url}), 200
    else:
        return jsonify({"error": "Failed to deploy", "details": response.text}), 500
