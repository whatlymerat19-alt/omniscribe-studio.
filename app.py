import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- TOUT LE DESIGN (HTML/CSS/JS) EST ICI ---
INTERFACE_COMPLETE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmniScribe Studio v3</title>
    <style>
        body { 
            background: #050505; color: #e0e0e0; 
            font-family: 'Segoe UI', sans-serif; 
            text-align: center; padding: 20px; margin: 0;
        }
        h1 { color: #ff0000; letter-spacing: 2px; font-size: 1.5rem; }
        .container { max-width: 400px; margin: auto; }
        
        textarea { 
            width: 100%; height: 100px; 
            background: #111; color: #fff; 
            border: 1px solid #333; border-radius: 8px;
            padding: 10px; box-sizing: border-box;
            margin-bottom: 15px;
        }

        .preview-box { 
            width: 100%; height: 450px; 
            background: #111; border: 2px solid #222;
            border-radius: 15px; margin-bottom: 20px;
            display: flex; align-items: center; justify-content: center;
            position: relative; overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }

        .overlay-text { 
            position: absolute; bottom: 50px; width: 80%;
            font-weight: bold; font-size: 1.2rem; text-shadow: 2px 2px 4px #000;
        }

        button { 
            width: 100%; padding: 15px; margin: 5px 0;
            border: none; border-radius: 8px;
            font-weight: bold; cursor: pointer; transition: 0.3s;
        }

        .btn-filter { background: #222; color: #aaa; border: 1px solid #444; }
        .btn-generate { 
            background: linear-gradient(45deg, #800, #b00); 
            color: white; font-size: 1.1rem; margin-top: 15px;
        }
        
        /* FILTRES */
        .sombre { filter: brightness(0.4) contrast(1.5); }
        .cinematic { filter: sepia(0.2) contrast(1.2); border-top: 25px solid black; border-bottom: 25px solid black; }
    </style>
</head>
<body>
    <div class="container">
        <h1>OMNISCRIBE MASTER</h1>
        <p style="font-size: 0.8rem; color: #666;">ALGORITHME DE MONTAGE v3.0</p>
        
        <textarea id="prompt" placeholder="Décrivez l'ambiance ou le texte pour Marcus..."></textarea>
        
        <div id="videoView" class="preview-box">
            <div id="textInside" class="overlay-text">VOTRE TEXTE ICI</div>
            <p style="color: #333;">APERÇU VIDÉO 9:16</p>
        </div>

        <button class="btn-filter" onclick="applyFilter('sombre')">FILTRE : SOMBRE</button>
        <button class="btn-filter" onclick="applyFilter('cinematic')">FILTRE : CINÉMA</button>
        
        <button class="btn-generate" onclick="generate()">GÉNÉRER AVEC MARCUS</button>
    </div>

    <script>
        function applyFilter(type) {
            document.getElementById('videoView').className = 'preview-box ' + type;
        }

        function generate() {
            const p = document.getElementById('prompt').value;
            if(!p) { alert("Entrez un prompt d'abord !"); return; }
            document.getElementById('textInside').innerText = p;
            alert("L'algorithme envoie la requête à l'API de Marcus...");
        }
    </script>
</body>
</html>
"""

# --- LOGIQUE DU SERVEUR ---

@app.route('/')
def home():
    return INTERFACE_COMPLETE

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "engine": "OmniScribe v3"})

if __name__ == "__main__":
    # Render utilise la variable d'environnement PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
