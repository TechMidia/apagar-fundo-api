# Usa uma imagem Python leve
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o container
COPY . .

# Comando para iniciar a API com uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
