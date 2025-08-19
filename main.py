from flask import Flask, request, jsonify
import zipfile, os, io, requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Webhook Publisher is Live!"

@app.route("/publish", methods=["POST"])
def publish():
    html_content = request.form.get("html")
    if not html_content:
        return jsonify({"error": "No HTML provided"}), 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        zipf.writestr("index.html", html_content)
    zip_buffer.seek(0)

    headers = {
        "Authorization": f"Bearer {os.getenv('NETLIFY_API_TOKEN')}"
    }

    files = {
        'file': ('site.zip', zip_buffer, 'application/zip')
    }

    site_id = os.getenv('NETLIFY_SITE_ID')
    url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
    response = requests.post(url, headers=headers, files=files)

    if response.status_code in [200, 201]:
        return jsonify({"message": "Deployed!", "url": response.json().get('deploy_ssl_url')})
    else:
        return jsonify({"error": "Deployment failed", "details": response.text}), 500
