from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome. App is running."

@app.route("/publish", methods=["POST"])
def publish():
    html = request.form.get("html")
    if not html:
        return jsonify({"error": "Missing 'html' in body"}), 400
    return jsonify({"message": "Received HTML!", "length": len(html)}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
