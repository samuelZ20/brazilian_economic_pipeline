import pandas as pd

def clean_bacen_data(df_bronze):
    """
    Aplica as regras de limpeza e tipagem da Camada Silver.
    """
    df = df_bronze.copy()
    
    # 1. Tipagem: Converter 'data' para datetime real
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    
    # 2. Tipagem: Converter 'valor' para float
    df['valor'] = df['valor'].astype(float)
    
    # 3. Deduplicação: Mantém apenas o último registro de cada data
    df = df.drop_duplicates(subset=['data'], keep='last')
    
    # 4. Auditoria: Adiciona timestamp de processamento
    df['processed_at'] = pd.Timestamp.now()
    
    return df.sort_values('data')
