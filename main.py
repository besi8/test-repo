from flask import Flask, request, jsonify
import os
import zipfile
import tempfile
import requests

app = Flask(__name__)

NETLIFY_TOKEN = os.environ.get("NETLIFY_TOKEN")

@app.route("/publish", methods=["POST"])
def publish():
    html = request.form.get("html")
    if not html:
        return jsonify({"error": "No HTML provided"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "index.html")
        with open(html_path, "w") as f:
            f.write(html)

        zip_path = os.path.join(tmpdir, "site.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(html_path, arcname="index.html")

        with open(zip_path, "rb") as f:
            response = requests.post(
                "https://api.netlify.com/api/v1/sites",
                headers={"Authorization": f"Bearer {NETLIFY_TOKEN}"},
                files={"file": ("site.zip", f)},
            )

        if response.status_code != 200:
            return jsonify({"error": "Failed to upload to Netlify", "details": response.text}), 500

        data = response.json()
        return jsonify({"url": data.get("url")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
