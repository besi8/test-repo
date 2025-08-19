from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_html():
    data = request.get_json()
    if not data or 'html' not in data:
        return jsonify({'error': 'Missing HTML data'}), 400

    html_content = data['html']
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    return jsonify({'message': 'HTML file saved successfully!'}), 200

# Opsionale për testim lokal:
@app.route('/', methods=['GET'])
def home():
    return 'Service is running', 200
