import os
import requests
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# On récupère ta clé secrète que tu as cachée dans Render
API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # L'ID de la voix de Marcus

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmniScribe Studio v3</title>
    <style>
        body { background: #050505; color: #e0e0e0; font-family: sans-serif; text-align: center; padding: 20px; }
        h1 { color: #ff0000; letter-spacing: 2px; }
        textarea { width: 100%; height: 80px; background: #111; color: #fff; border: 1px solid #333; border-radius: 8px; padding: 10px; margin-bottom: 10px; }
        .preview-box { width: 100%; height: 400px; background: #111; border: 2px solid #222; border-radius: 15px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
        button { width: 100%; padding: 15px; margin: 5px 0; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .btn-generate { background: #800; color: white; }
    </style>
</head>
<body>
    <h1>OMNISCRIBE MASTER</h1>
    <textarea id="prompt" placeholder="Texte pour Marcus..."></textarea>
    <div class="preview-box" id="vView">APERÇU</div>
    <audio id="audioPlayer" controls style="display:none; width:100%; margin-top:10px;"></audio>
    <button class="btn-generate" id="genBtn" onclick="generateVoice()">PARLER AVEC MARCUS</button>

    <script>
        async function generateVoice() {
            const text = document.getElementById('prompt').value;
            const btn = document.getElementById('genBtn');
            const player = document.getElementById('audioPlayer');
            
            if(!text) return alert("Écris un texte !");
            
            btn.innerText = "MARCUS RÉFLÉCHIT...";
            btn.disabled = true;

            const response = await fetch('/speak', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            });

            if(response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                player.src = url;
                player.style.display = "block";
                player.play();
            } else {
                alert("Erreur API. Vérifie ta clé sur Render !");
            }
            btn.innerText = "PARLER AVEC MARCUS";
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_CONTENT

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {"text": text, "model_id": "eleven_multilingual_v2"}

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return Response(response.content, mimetype="audio/mpeg")
    return jsonify({"error": "Failed"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
