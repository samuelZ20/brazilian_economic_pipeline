import os
from deltalake.writer import write_deltalake
from dotenv import load_dotenv

load_dotenv()

class DeltaManager:
    def __init__(self):
        """
        Gerencia configurações de storage para Delta Lake e Pandas.
        """
        # Opções para Delta Lake (delta-rs)
        self.delta_storage_options = {
            "AWS_ENDPOINT_URL": os.getenv('MINIO_ENDPOINT'),
            "AWS_ACCESS_KEY_ID": os.getenv('MINIO_ACCESS_KEY'),
            "AWS_SECRET_ACCESS_KEY": os.getenv('MINIO_SECRET_KEY'),
            "AWS_REGION": "us-east-1",
            "AWS_ALLOW_HTTP": "true",
            "AWS_S3_ALLOW_UNSAFE_DISABLE_SSL": "true"
        }
        
        # Opções para Pandas (s3fs) - Ajustado para maior compatibilidade
        self.pandas_storage_options = {
            "key": os.getenv('MINIO_ACCESS_KEY'),
            "secret": os.getenv('MINIO_SECRET_KEY'),
            "use_ssl": False, # Força HTTP para o MinIO local
            "client_kwargs": {
                "endpoint_url": os.getenv('MINIO_ENDPOINT')
            }
        }

    def write_to_silver(self, df, serie_id):
        """Escreve a Delta Table na camada Silver."""
        bucket = os.getenv('MINIO_BUCKET')
        table_path = f"s3://{bucket}/silver/serie_{serie_id}"
        
        write_deltalake(
            table_path,
            df,
            mode="overwrite",
            storage_options=self.delta_storage_options
        )
        print(f"✅ Delta Table atualizada: {table_path}")
