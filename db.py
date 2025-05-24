import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Nome do banco (você pode trocar para outro se quiser)
db = client['encartes']

# Coleção onde vamos salvar os produtos
colecao_produtos = db['produtos_imagem']
