import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def get_minio_client():
    """
    Cria e retorna um cliente Boto3 configurado para o MinIO local.
    """
    return boto3.client(
        's3',
        endpoint_url=os.getenv('MINIO_ENDPOINT'),
        aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('MINIO_SECRET_KEY'),
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

def ensure_bucket_exists():
    """
    Garante que o bucket principal (bacen-lake) exista no MinIO.
    Substitui o papel de 'inicialização' de bancos tradicionais.
    """
    s3 = get_minio_client()
    bucket_name = os.getenv('MINIO_BUCKET')
    
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' já existe.")
    except:
        print(f"📦 Criando bucket '{bucket_name}' no MinIO...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"🚀 Bucket '{bucket_name}' criado com sucesso!")

if __name__ == "__main__":
    ensure_bucket_exists()
