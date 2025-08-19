from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Aktivizo logimin në Render (ose lokalisht)
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "✅ Aplikacioni është gjallë!",
        "message": "Flask serveri është ngritur me sukses dhe pret kërkesa në /publish."
    }), 200

@app.route("/publish", methods=["POST"])
def publish():
    html_content = request.form.get("html")

    if not html_content:
        logging.warning("❌ Parametri 'html' mungon në kërkesë.")
        return jsonify({
            "error": "Parametri 'html' është i detyrueshëm."
        }), 400

    logging.info(f"✅ HTML u mor me sukses. Gjatësia: {len(html_content)} karaktere.")
    
    # Opsionale: këtu mund të ruash HTML-n ose të bësh publikimin në Netlify, etj.
    
    return jsonify({
        "status": "success",
        "message": "HTML u pranua me sukses.",
        "preview": html_content[:60] + "..."  # tregojmë një pjesë të përmbajtjes
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # port i zakonshëm për Render (por jo i detyrueshëm)
