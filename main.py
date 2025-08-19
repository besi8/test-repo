from flask import Flask, request, jsonify
import os
import zipfile
import tempfile
import requests
import time

app = Flask(__name__)

NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")
NETLIFY_ACCOUNT = os.getenv("NETLIFY_ACCOUNT", "Besi Masha")

@app.route("/publish", methods=["POST"])
def publish():
    html_content = request.form.get("html")
    if not html_content:
        return jsonify({"error": "Missing 'html' field"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        zip_path = os.path.join(tmpdir, "site.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(html_path, arcname="index.html")

        headers = {
            "Authorization": f"Bearer {NETLIFY_TOKEN}",
        }

        with open(zip_path, "rb") as f:
            response = requests.post(
                "https://api.netlify.com/api/v1/sites",
                headers=headers,
                files={"file": ("site.zip", f)},
            )

        if response.status_code != 200:
            return jsonify({"error": "Netlify upload failed", "details": response.text}), 500

        site_data = response.json()
        return jsonify({
            "site_url": site_data.get("url"),
            "site_id": site_data.get("id"),
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
