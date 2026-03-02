import os
import pandas as pd
from dotenv import load_dotenv
from src.delta_manager import DeltaManager
from src.analytics import calculate_real_interest

load_dotenv()

def run_gold_pipeline():
    dm = DeltaManager()
    bucket = os.getenv('MINIO_BUCKET')
    storage_options = dm.delta_storage_options # Usamos a opção de leitura Delta

    print("🥇 Iniciando Processamento da Camada Gold...")

    try:
        # 1. Leitura das Delta Tables da Silver
        path_selic = f"s3://{bucket}/silver/serie_11"
        path_ipca = f"s3://{bucket}/silver/serie_433"
        
        # O delta-rs permite ler a tabela como DataFrame diretamente
        from deltalake import DeltaTable
        df_selic = DeltaTable(path_selic, storage_options=storage_options).to_pandas()
        df_ipca = DeltaTable(path_ipca, storage_options=storage_options).to_pandas()
        
        # 2. Transformação Gold (Analytics)
        df_gold = calculate_real_interest(df_selic, df_ipca)
        
        # 3. Salvando a tabela final na Gold
        dm.write_to_gold(df_gold, "economic_indicators_comparison")
        
    except Exception as e:
        print(f"❌ Erro na geração da Gold: {e}")

if __name__ == "__main__":
    # Nota: Precisamos adicionar o método write_to_gold no seu DeltaManager
    run_gold_pipeline()
