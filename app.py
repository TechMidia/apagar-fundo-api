from flask import Flask, request, jsonify
import os
from datetime import datetime
from pymongo import MongoClient, errors as mongo_errors
import boto3
import requests

app = Flask(__name__)

# Testa MongoDB
def testar_mongodb():
    try:
        mongo_uri = os.environ.get('MONGO_URI')
        if not mongo_uri:
            return 'Variável MONGO_URI não encontrada'
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        client.server_info()  # força teste de conexão
        return 'MongoDB conectado com sucesso'
    except mongo_errors.PyMongoError as e:
        return f'Erro MongoDB: {e}'

# Testa S3
def testar_s3():
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION')
        )
        s3.list_buckets()  # testa acesso
        return 'AWS S3 conectado com sucesso'
    except Exception as e:
        return f'Erro S3: {e}'

# Testa API Dezgo
def testar_dezgo():
    try:
        api_key = os.environ.get('DEZGO_API_KEY')
        if not api_key:
            return 'Chave da API Dezgo não encontrada'
        response = requests.post(
            'https://api.dezgo.com/remove-background',
            headers={'X-Dezgo-Key': api_key},
            files={'image': ('test.png', b'test')}
        )
        return f'Dezgo: código {response.status_code}'
    except Exception as e:
        return f'Erro na chamada Dezgo: {e}'

@app.route('/')
def home():
    resultados = {
        'status': 'API ativa',
        'mongo': testar_mongodb(),
        's3': testar_s3(),
        'dezgo': testar_dezgo()
    }
    return jsonify(resultados)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
