from flask import Flask, request, jsonify
import zipfile
import io
import requests
import os

app = Flask(__name__)

# Merr variablat nga ambienti i Render
NETLIFY_SITE_ID = os.getenv("NETLIFY_SITE_ID")
NETLIFY_TOKEN = os.getenv("NETLIFY_TOKEN")

@app.route("/", methods=["GET"])
def index():
    return "✅ Aplikacioni është gjallë!"

@app.route("/publish", methods=["POST"])
def publish():
    html_content = request.form.get("html")
    if not html_content:
        return jsonify({"error": "HTML content is missing"}), 400

    # Krijo ZIP me index.html
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr("index.html", html_content)
    zip_buffer.seek(0)

    # Dërgo në Netlify
    url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys"
    headers = {
        "Authorization": f"Bearer {NETLIFY_TOKEN}"
    }
    files = {
        "file": ("site.zip", zip_buffer, "application/zip")
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code in [200, 201]:
        return jsonify({
            "message": "Deploy successful",
            "netlify_url": response.json().get("deploy_ssl_url")
        }), 200
    else:
        return jsonify({
            "error": "Deploy failed",
            "details": response.text
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
