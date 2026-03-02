import os
from api_client import BacenAPIClient
from db_manager import upload_file, ensure_bucket_exists
from utils import generate_lake_path, save_to_parquet

def run_ingestion():
    # 1. Preparação do ambiente
    ensure_bucket_exists()
    client = BacenAPIClient()
    
    print("🎬 Iniciando Ingestão na Camada Bronze...")
    series_data = client.get_all_series()
    
    for sid, data in series_data.items():
        # 2. Organiza o caminho no estilo Hive (Partitioning)
        lake_folder = generate_lake_path('bronze', sid)
        s3_path = f"{lake_folder}/data.parquet"
        
        # 3. Salva localmente em formato binário otimizado
        temp_local_path = f"data/temp_serie_{sid}.parquet"
        save_to_parquet(data, temp_local_path)
        
        # 4. Upload para o storage persistente
        success = upload_file(temp_local_path, s3_path)
        
        # 5. Limpeza de arquivos temporários
        if success and os.path.exists(temp_local_path):
            os.remove(temp_local_path)

    print("🏁 Ingestão Bronze finalizada com sucesso!")

if __name__ == "__main__":
    run_ingestion()
