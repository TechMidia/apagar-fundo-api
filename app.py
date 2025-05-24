from flask import Flask, request, send_file
import requests
import os
from datetime import datetime
from pymongo import MongoClient
import boto3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Conexão com MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['encartes']
colecao_produtos = db['produtos_imagem']

# Conexão com Amazon S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION')
)
bucket_name = os.environ.get('AWS_S3_BUCKET')

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

    response = requests.post(
        'https://api.dezgo.com/remove-background',
        headers={'X-Dezgo-Key': api_key},
        files={'image': image.read()}
    )

    if response.status_code != 200:
        return {'error': 'Erro na API Dezgo', 'status': response.status_code}, 500

    # Nome seguro para o arquivo
    timestamp = int(datetime.now().timestamp())
    nome_arquivo = secure_filename(f'{nome_produto}_{timestamp}.png')

    # Salva temporariamente a imagem
    with open(nome_arquivo, 'wb') as f:
        f.write(response.content)

    # Faz o upload para o S3
    s3.upload_file(nome_arquivo, bucket_name, nome_arquivo)
    url_s3 = f"https://{bucket_name}.s3.amazonaws.com/{nome_arquivo}"

    # Salva no MongoDB
    produto = {
        'nome': nome_produto,
        'tipo': 'desconhecido',
        'imagem_url': 'imagem_original_nao_salva',
        'imagem_fundo_removido_url': url_s3,
        'origem': 'upload',
        'criado_em': datetime.now()
    }

    colecao_produtos.insert_one(produto)

    # Remove imagem local
    os.remove(nome_arquivo)

    return {'mensagem': 'Upload feito com sucesso', 'url_imagem_s3': url_s3}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
