import os
from deltalake.writer import write_deltalake
from dotenv import load_dotenv

load_dotenv()

class DeltaManager:
    def __init__(self):
        """
        Gerencia as configurações de storage para o ecossistema Delta Lake.
        """
        self.bucket = os.getenv('MINIO_BUCKET')
        # Configurações para o motor Delta (Rust)
        self.delta_storage_options = {
            "AWS_ENDPOINT_URL": os.getenv('MINIO_ENDPOINT'),
            "AWS_ACCESS_KEY_ID": os.getenv('MINIO_ACCESS_KEY'),
            "AWS_SECRET_ACCESS_KEY": os.getenv('MINIO_SECRET_KEY'),
            "AWS_REGION": "us-east-1",
            "AWS_ALLOW_HTTP": "true",
            "AWS_S3_ALLOW_UNSAFE_DISABLE_SSL": "true"
        }
        
        # Opções para compatibilidade com Pandas (s3fs)
        self.pandas_storage_options = {
            "key": os.getenv('MINIO_ACCESS_KEY'),
            "secret": os.getenv('MINIO_SECRET_KEY'),
            "use_ssl": False,
            "client_kwargs": {
                "endpoint_url": os.getenv('MINIO_ENDPOINT')
            }
        }

    def _write_delta(self, df, layer, table_name):
        """Método privado para evitar repetição de código (DRY)."""
        path = f"s3://{self.bucket}/{layer}/{table_name}"
        write_deltalake(
            path,
            df,
            mode="overwrite",
            storage_options=self.delta_storage_options
        )
        print(f"✅ Tabela Delta atualizada em {layer.upper()}: {path}")

    def write_to_silver(self, df, serie_id):
        self._write_delta(df, "silver", f"serie_{serie_id}")

    def write_to_gold(self, df, table_name):
        """Salva o dado refinado para analytics na Camada Gold."""
        self._write_delta(df, "gold", table_name)
