import os
from flask import Flask, send_from_directory, jsonify

# On force Flask à regarder dans le dossier actuel
app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    # Cette ligne cherche index.html à la racine
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
