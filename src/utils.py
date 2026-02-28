import os
import pandas as pd
from datetime import datetime

def generate_lake_path(layer, serie_id):
    """
    Gera o caminho organizado por camada, série e data atual.
    Exemplo: bronze/serie_11/year=2026/month=02/data.parquet
    """
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    
    path = f"{layer}/serie_{serie_id}/year={year}/month={month}"
    return path

def save_to_parquet(data, filename):
    """
    Converte a lista de dicionários da API em um DataFrame e salva localmente temporário.
    """
    df = pd.DataFrame(data)
    # Garante que a pasta temporária exista
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_parquet(filename, index=False)
    print(f"📄 Arquivo local gerado: {filename}")
    return filename
