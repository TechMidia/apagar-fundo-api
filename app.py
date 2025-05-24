from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
from pymongo import MongoClient
import boto3
import requests

app = Flask(__name__)

# MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['encartes']
colecao_produtos = db['produtos_imagem']

# AWS S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION')

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@app.route('/')
def home():
    return 'API de Remoção de Fundo ativa!'

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    if 'file' not in request.files or 'nome' not in request.form:
        return jsonify({'error': 'Imagem e nome do produto são obrigatórios'}), 400

    image = request.files['file']
    nome_produto = request.form['nome']

    return jsonify({
        'mensagem': 'Recebido com sucesso',
        'nome_produto': nome_produto,
        'nome_arquivo': image.filename
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
