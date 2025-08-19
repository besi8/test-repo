from flask import Flask, request, jsonify
import zipfile, io, requests

app = Flask(__name__)

NETLIFY_SITE_ID = "ea2c01c6-c2b6-46e3-ab7a-135b45af3838"
NETLIFY_API_TOKEN = "nfp_G1fwnnWwkQPTB9xrFZ8QWXVdYxgYbxmW6f11"

@app.route('/')
def home():
    return "Webhook Publisher is Live!"

@app.route('/publish', methods=['POST'])
def publish():
    html_content = request.form.get("html")
    if not html_content:
        return jsonify({"error": "No HTML provided"}), 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        zipf.writestr("index.html", html_content)
    zip_buffer.seek(0)

    headers = {
        "Authorization": f"Bearer {NETLIFY_API_TOKEN}"
    }
    files = {
        'file': ('site.zip', zip_buffer, 'application/zip')
    }
    url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys"
    response = requests.post(url, headers=headers, files=files)

    if response.status_code in [200, 201]:
        return jsonify({
            "message": "Deployed!",
            "url": response.json().get('deploy_ssl_url')
        })
    else:
        return jsonify({
            "error": "Deployment failed",
            "details": response.text
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
