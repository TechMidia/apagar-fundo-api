import boto3
import os
from botocore.exceptions import NoCredentialsError

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
