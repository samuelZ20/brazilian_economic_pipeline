import pandas as pd

def calculate_real_interest(df_selic, df_ipca):
    """
    Calcula o Juro Real aproximado cruzando Selic e IPCA.
    """
    # 1. Alinha as colunas para o Join
    df_selic = df_selic[['data', 'valor']].rename(columns={'valor': 'selic'})
    df_ipca = df_ipca[['data', 'valor']].rename(columns={'valor': 'ipca'})
    
    # 2. Faz o merge das duas séries pela data
    df_gold = pd.merge(df_selic, df_ipca, on='data', how='inner')
    
    # 3. Cálculo do Juro Real (Simplificado para fins didáticos)
    # Em produção, usa-se a fórmula de Fisher: ((1 + selic) / (1 + ipca)) - 1
    df_gold['juro_real'] = df_gold['selic'] - df_gold['ipca']
    
    # 4. Adiciona média móvel de 12 meses para suavizar tendências
    df_gold['selic_ma_12'] = df_gold['selic'].rolling(window=12).mean()
    
    return df_gold.sort_values('data', ascending=False)
