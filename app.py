from flask import Flask, request, send_file
import requests
import os
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Conexão com MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['encartes']  # nome do banco
colecao_produtos = db['produtos_imagem']  # nome da coleção

@app.route('/')
def home():
    return 'API de Remoção de Fundo ativa!'

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    if 'file' not in request.files or 'nome' not in request.form:
        return {'error': 'Imagem e nome do produto são obrigatórios'}, 400

    image = request.files['file']
    nome_produto = request.form['nome']
    api_key = os.environ.get('DEZGO_API_KEY')

    if not api_key:
        return {'error': 'Chave da API não configurada'}, 500

    # Envia para a API do Dezgo
    response = requests.post(
        'https://api.dezgo.com/remove-background',
        headers={'X-Dezgo-Key': api_key},
        files={'image': image.read()}
    )

    if response.status_code != 200:
        return {'error': 'Erro na API Dezgo', 'status': response.status_code}, 500

    # Salva imagem local
    nome_arquivo = f'imagem_sem_fundo_{datetime.now().timestamp()}.png'
    with open(nome_arquivo, 'wb') as f:
        f.write(response.content)

    # Salva no MongoDB
    produto = {
        'nome': nome_produto,
        'tipo': 'desconhecido',
        'imagem_url': 'imagem_original_nao_salva',
        'imagem_fundo_removido_url': nome_arquivo,
        'origem': 'upload',
        'criado_em': datetime.now()
    }

    colecao_produtos.insert_one(produto)

    return send_file(nome_arquivo, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
