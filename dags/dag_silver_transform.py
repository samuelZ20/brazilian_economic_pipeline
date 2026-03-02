import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from src.delta_manager import DeltaManager
from src.transform import clean_bacen_data

load_dotenv()

def run_silver_pipeline(target_month=None):
    dm = DeltaManager()
    bucket = os.getenv('MINIO_BUCKET')
    series_ids = os.getenv('SERIES_IDS', '').split(',')
    
    # Se não passarmos um mês, ele usa o mês atual (03)
    month = target_month if target_month else datetime.now().strftime('%m')
    year = datetime.now().strftime('%Y')
    
    print(f"🥈 Iniciando Transformação Bronze -> Silver (Referência: {month}/{year})...")

    for sid in series_ids:
        sid = sid.strip()
        # Caminho dinâmico baseado na partição
        path_bronze = f"s3://{bucket}/bronze/serie_{sid}/year={year}/month={month}/data.parquet"
        
        try:
            # Lendo com as opções de compatibilidade do Pandas
            df_raw = pd.read_parquet(path_bronze, storage_options=dm.pandas_storage_options)
            
            df_clean = clean_bacen_data(df_raw)
            dm.write_to_silver(df_clean, sid)
            
        except Exception as e:
            print(f"⚠️ Pulo na série {sid}: Pasta {month}/{year} não encontrada ou erro no S3. Detalhes: {e}")

if __name__ == "__main__":
    # TENTATIVA 1: Tenta o mês atual. Se falhar, você pode rodar manualmente para o mês 02
    run_silver_pipeline(target_month="02")
