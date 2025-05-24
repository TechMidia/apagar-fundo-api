import os
import requests
from flask import Flask, request, send_file
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)

DEZGO_API_KEY = os.getenv("DEZGO_API_KEY")

@app.route("/remover-fundo", methods=["POST"])
def remover_fundo():
    if "file" not in request.files:
        return {"erro": "Arquivo não enviado"}, 400

    imagem = request.files["file"]

    headers = {
        "Authorization": f"Bearer {DEZGO_API_KEY}"
    }

    files = {
        "image": (imagem.filename, imagem.stream, imagem.mimetype)
    }

    url = "https://api.dezgo.com/background-removal"

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return {"erro": "Erro ao remover fundo", "detalhes": response.text}, 500

    return send_file(BytesIO(response.content), mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
