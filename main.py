from flask import Flask, request, jsonify
import zipfile, io, requests
import os

app = Flask(__name__)

NETLIFY_SITE_ID = "ea2c01c6-c2b6-46e3-ab7a-135b45af3838"
NETLIFY_API_TOKEN = "nfp_G1fwnnWwkQPTB9xrFZ8QWXVdYxgYbxmW6f11"

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "✅ Server is running",
        "message": "Use POST /publish to deploy HTML to Netlify."
    })

@app.route("/publish", methods=["POST"])
def publish():
    html = request.form.get("html")
    if not html:
        return jsonify({"error": "No HTML provided"}), 400

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("index.html", html)
    zip_buffer.seek(0)

    response = requests.post(
        f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys",
        headers={"Authorization": f"Bearer {NETLIFY_API_TOKEN}"},
        files={"file": ("site.zip", zip_buffer, "application/zip")}
    )

    if response.status_code in [200, 201]:
        return jsonify({"url": response.json().get("deploy_ssl_url")})
    else:
        return jsonify({"error": "Deployment failed", "details": response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
