import os
import requests
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
# ID par défaut de la voix (Adam), tu pourras le changer plus tard
VOICE_ID = "pNInz6obpgDQGcFmaJgB" 

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OmniScribe Master</title>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        textarea { width: 100%; height: 80px; background: #111; color: #fff; border: 1px solid #333; padding: 10px; border-radius: 8px; }
        .btn-generate { background: #800; color: white; width: 100%; padding: 15px; border: none; border-radius: 8px; font-weight: bold; margin-top: 10px; cursor: pointer; }
        #status { margin-top: 10px; font-size: 0.8rem; color: #666; }
    </style>
</head>
<body>
    <h1>OMNISCRIBE MASTER</h1>
    <textarea id="prompt" placeholder="Message pour Marcus..."></textarea>
    <button class="btn-generate" id="genBtn" onclick="generateVoice()">PARLER AVEC MARCUS</button>
    <div id="status"></div>
    <audio id="audioPlayer" controls style="display:none; width:100%; margin-top:20px;"></audio>

    <script>
        async function generateVoice() {
            const text = document.getElementById('prompt').value;
            const btn = document.getElementById('genBtn');
            const status = document.getElementById('status');
            const player = document.getElementById('audioPlayer');
            
            if(!text) return alert("Écris un message !");
            
            btn.innerText = "CONNEXION À MARCUS...";
            btn.disabled = true;
            status.innerText = "Envoi de la requête...";

            try {
                const response = await fetch('/speak', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });

                const data = await response.json();

                if(response.ok && data.audio) {
                    const audioBlob = await (await fetch("data:audio/mpeg;base64," + data.audio)).blob();
                    player.src = URL.createObjectURL(audioBlob);
                    player.style.display = "block";
                    player.play();
                    status.innerText = "Succès !";
                } else {
                    status.innerText = "Erreur : " + (data.error || "Inconnue");
                    alert("Erreur : " + (data.details || "Vérifie ta clé API"));
                }
            } catch (e) {
                status.innerText = "Erreur réseau";
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
    
    if not API_KEY:
        return jsonify({"error": "Clé manquante", "details": "La variable ELEVENLABS_API_KEY n'est pas configurée sur Render"}), 500

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            import base64
            audio_b64 = base64.b64encode(res.content).decode('utf-8')
            return jsonify({"audio": audio_b64})
        else:
            return jsonify({"error": "API ElevenLabs", "details": res.text}), res.status_code
    except Exception as e:
        return jsonify({"error": "Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
