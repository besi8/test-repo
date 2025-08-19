from flask import Flask, request, jsonify
import os
import zipfile
import tempfile
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "html" not in data or "site_name" not in data or "netlify_token" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    html_content = data["html"]
    site_name = data["site_name"]
    netlify_token = data["netlify_token"]

    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            html_path = os.path.join(tmpdirname, "index.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            zip_path = os.path.join(tmpdirname, "site.zip")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                zipf.write(html_path, "index.html")

            with open(zip_path, "rb") as f:
                headers = {
                    "Authorization": f"Bearer {netlify_token}"
                }
                response = requests.post(
                    "https://api.netlify.com/api/v1/sites",
                    headers=headers,
                    files={"file": ("site.zip", f, "application/zip")},
                    data={"name": site_name}
                )
            return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
