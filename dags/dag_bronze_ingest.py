import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from src.api_client import BacenAPIClient
from src.db_manager import upload_file, ensure_bucket_exists
from src.utils import generate_lake_path, save_to_parquet
from dotenv import load_dotenv

load_dotenv()

def run_ingestion():
    ensure_bucket_exists()
    client = BacenAPIClient()
    
    # Lógica Dinâmica
    now = datetime.now()
    month = now.strftime('%m')
    year = now.strftime('%Y')
    
    print(f"🎬 Ingestão Bronze Dinâmica: Referência {month}/{year}")
    series_data = client.get_all_series()
    
    for sid, data in series_data.items():
        # O generate_lake_path já deve ser dinâmico internamente
        lake_folder = generate_lake_path('bronze', sid)
        s3_path = f"{lake_folder}/data.parquet"
        
        temp_local_path = f"data/temp_serie_{sid}.parquet"
        save_to_parquet(data, temp_local_path)
        upload_file(temp_local_path, s3_path)
        
        if os.path.exists(temp_local_path):
            os.remove(temp_local_path)

    print("🏁 Ingestão Bronze finalizada!")

with DAG('1_camada_bronze', start_date=datetime(2026, 1, 1), schedule_interval=None, catchup=False) as dag:
    task_ingest = PythonOperator(
        task_id='ingestao_bacen', 
        python_callable=run_ingestion
    )
    
    # Ao terminar, chama a próxima DAG do README
    trigger_silver = TriggerDagRunOperator(
        task_id='chamar_silver',
        trigger_dag_id='2_camada_silver'
    )
    
    task_ingest >> trigger_silver

if __name__ == "__main__":
    run_ingestion()
