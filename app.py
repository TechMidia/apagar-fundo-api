from flask import Flask, request, send_file, jsonify
import requests
import os
from datetime import datetime
from pymongo import MongoClient
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Conexão com MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['encartes']  # nome do banco
colecao_produtos = db['produtos_imagem']  # nome da coleção

# Função para upload no Amazon S3
def upload_para_s3(caminho_arquivo, nome_arquivo_s3):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )
    bucket = os.environ.get('AWS_S3_BUCKET')
    try:
        s3.upload_file(caminho_arquivo, bucket, nome_arquivo_s3)
        url = f"https://{bucket}.s3.{os.environ.get('AWS_REGION')}.amazonaws.com/{nome_arquivo_s3}"
        return url
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except NoCredentialsError:
        print("Credenciais não encontradas.")
    return None

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

    # Envia para o S3
    nome_arquivo_s3 = f'produtos/{nome_arquivo}'
    url_imagem_s3 = upload_para_s3(nome_arquivo, nome_arquivo_s3)

    if not url_imagem_s3:
        return {'error': 'Falha ao enviar para o S3'}, 500

    # Salva no MongoDB
    produto = {
        'nome': nome_produto,
        'tipo': 'desconhecido',
        'imagem_url': 'imagem_original_nao_salva',
        'imagem_fundo_removido_url': url_imagem_s3,
        'origem': 'upload',
        'criado_em': datetime.now()
    }

    colecao_produtos.insert_one(produto)

    return jsonify({'imagem_url': url_imagem_s3})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
