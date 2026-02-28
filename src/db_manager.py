import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (chaves e endpoints)
load_dotenv()

def get_minio_client():
    """
    Cria e retorna o cliente Boto3 configurado para o MinIO local.
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
    Garante que o bucket principal (bacen-lake) esteja criado.
    """
    s3 = get_minio_client()
    bucket_name = os.getenv('MINIO_BUCKET')
    try:
        s3.head_bucket(Bucket=bucket_name)
    except:
        print(f"📦 Criando bucket '{bucket_name}' no MinIO...")
        s3.create_bucket(Bucket=bucket_name)

def upload_file(local_path, s3_path):
    """
    O 'Braço' do Python: Pega um arquivo local e arremessa para o MinIO.
    """
    s3 = get_minio_client()
    bucket = os.getenv('MINIO_BUCKET')
    try:
        s3.upload_file(local_path, bucket, s3_path)
        print(f"🚀 Upload concluído com sucesso: {s3_path}")
        return True
    except Exception as e:
        print(f"❌ Erro crítico no upload para {s3_path}: {e}")
        return False

if __name__ == "__main__":
    # Teste de inicialização
    ensure_bucket_exists()
