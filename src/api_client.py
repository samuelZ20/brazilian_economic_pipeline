import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class BacenAPIClient:
    def __init__(self):
        self.base_url = os.getenv('BACEN_BASE_URL')
        self.series_ids = os.getenv('SERIES_IDS', '').split(',')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

    def fetch_data(self, series_id, days_back=730):
        """
        Busca os dados dos últimos 2 anos para evitar sobrecarga e erro 406.
        """
        end_date = datetime.now().strftime('%d/%m/%Y')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%d/%m/%Y')
        
        url = f"{self.base_url}.{series_id.strip()}/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"
        print(f"🔍 Buscando série {series_id} (desde {start_date})...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na série {series_id}: {e}")
            return None

    def get_all_series(self):
        all_data = {}
        for sid in self.series_ids:
            data = self.fetch_data(sid.strip())
            if data:
                all_data[sid.strip()] = data
        return all_data

if __name__ == "__main__":
    client = BacenAPIClient()
    results = client.get_all_series()
    for sid, data in results.items():
        print(f"✅ Série {sid}: {len(data)} registros encontrados.")