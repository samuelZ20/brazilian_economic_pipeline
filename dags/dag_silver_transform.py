import os
import sys
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from src.delta_manager import DeltaManager
from src.transform import clean_bacen_data

load_dotenv()

def run_silver_pipeline(target_month=None, target_year=None):
    dm = DeltaManager()
    bucket = os.getenv('MINIO_BUCKET')
    series_ids = os.getenv('SERIES_IDS', '').split(',')
    
    # Lógica Híbrida: Prioriza argumento, senão usa o "agora"
    now = datetime.now()
    month = target_month if target_month else now.strftime('%m')
    year = target_year if target_year else now.strftime('%Y')
    
    print(f"🥈 Transformação Silver: Processando partição {month}/{year}...")

    for sid in series_ids:
        sid = sid.strip()
        path_bronze = f"s3://{bucket}/bronze/serie_{sid}/year={year}/month={month}/data.parquet"
        
        try:
            df_raw = pd.read_parquet(path_bronze, storage_options=dm.pandas_storage_options)
            df_clean = clean_bacen_data(df_raw)
            dm.write_to_silver(df_clean, sid)
        except Exception as e:
            print(f"⚠️ Pulo na série {sid}: {e}")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

with DAG('2_camada_silver', start_date=datetime(2026, 1, 1), schedule_interval=None, catchup=False) as dag:
    task_transform = PythonOperator(
        task_id='transform_bronze_to_silver',
        python_callable=run_silver_pipeline
    )
    
    trigger_gold = TriggerDagRunOperator(
        task_id='chamar_gold',
        trigger_dag_id='3_camada_gold'
    )
    
    task_transform >> trigger_gold

if __name__ == "__main__":
    # Permite rodar: python -m dags.dag_silver_transform 02 2026
    arg_month = sys.argv[1] if len(sys.argv) > 1 else None
    arg_year = sys.argv[2] if len(sys.argv) > 2 else None
    
    run_silver_pipeline(target_month=arg_month, target_year=arg_year)
