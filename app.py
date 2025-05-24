from flask import Flask, request, send_file
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'API de Remoção de Fundo ativa!'

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    if 'file' not in request.files:
        return {'error': 'Nenhuma imagem enviada'}, 400

    image = request.files['file']
    api_key = os.environ.get('DEZGO_API_KEY')

    if not api_key:
        return {'error': 'Chave da API não configurada'}, 500

    response = requests.post(
        'https://api.dezgo.com/remove-background',
        headers={'X-Dezgo-Key': api_key},
        files={'image': image.read()}
    )

    if response.status_code != 200:
        return {'error': 'Erro na API Dezgo', 'status': response.status_code}, 500

    with open('imagem_sem_fundo.png', 'wb') as f:
        f.write(response.content)

    return send_file('imagem_sem_fundo.png', mimetype='image/png')
