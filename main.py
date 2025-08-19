from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Live"

@app.route("/publish", methods=["POST"])
def publish():
    return "✅ Publish endpoint funksionon", 200
