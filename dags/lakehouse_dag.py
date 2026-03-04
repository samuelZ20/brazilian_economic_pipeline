from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importamos as funções que você já testou e validou!
from dag_bronze_ingest import run_ingestion
from dag_silver_transform import run_silver_pipeline
from dag_gold_analytics import run_gold_pipeline

default_args = {
    'owner': 'samuel_frizzone',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'brazilian_economic_lakehouse',
    default_args=default_args,
    description='Pipeline de ponta a ponta: API Bacen -> Bronze -> Silver -> Gold',
    schedule_interval='@daily',    
    catchup=False
) as dag:

    # 1. Tarefa de Ingestão (Bronze)
    task_bronze = PythonOperator(
        task_id='ingest_bacen_to_bronze',
        python_callable=run_ingestion
    )

    # 2. Tarefa de Refino (Silver)
    task_silver = PythonOperator(
        task_id='transform_bronze_to_silver',
        python_callable=run_silver_pipeline
    )

    # 3. Tarefa de Analytics (Gold)
    task_gold = PythonOperator(
        task_id='generate_gold_indicators',
        python_callable=run_gold_pipeline
    )

    # Definindo a Orquestração (O Fluxo)
    task_bronze >> task_silver >> task_gold
