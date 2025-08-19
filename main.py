import os
import zipfile
import tempfile
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NETLIFY_API_URL = "https://api.netlify.com/api/v1/sites"
NETLIFY_SITE_ID = os.getenv("NETLIFY_SITE_ID")
NETLIFY_ACCESS_TOKEN = os.getenv("NETLIFY_ACCESS_TOKEN")

@app.route("/publish", methods=["POST"])
def publish():
    html_content = request.form.get("html")
    if not html_content:
        return jsonify({"error": "Missing HTML content"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        zip_path = os.path.join(temp_dir, "site.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(html_path, arcname="index.html")

        with open(zip_path, "rb") as zip_file:
            headers = {
                "Authorization": f"Bearer {NETLIFY_ACCESS_TOKEN}"
            }
            files = {
                "file": ("site.zip", zip_file, "application/zip")
            }
            response = requests.post(
                f"{NETLIFY_API_URL}/{NETLIFY_SITE_ID}/deploys",
                headers=headers,
                files=files
            )

        if response.status_code == 200:
            return jsonify({"message": "Deploy successful", "deploy_url": response.json().get("deploy_url")})
        else:
            return jsonify({"error": "Deploy failed", "details": response.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
