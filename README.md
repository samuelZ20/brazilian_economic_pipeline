# 🏦 Brazilian Economic Indicators — Delta Lake Pipeline

Pipeline de dados **End-to-End** que extrai indicadores econômicos do Banco Central do Brasil (BACEN), processa através da arquitetura **Medallion** e armazena em um **Delta Lake local utilizando MinIO**.

---

## 🏗️ Arquitetura

O fluxo segue uma orquestração rígida onde a infraestrutura é validada antes do processamento dos dados.

### 📌 Diagrama do Fluxo

```mermaid
flowchart TD
    API([BACEN SGS API]) -->|REST JSON| BRONZE

    subgraph INFRA ["Infraestrutura"]
        SETUP["dag_setup_db — @once"]:::infra
        CHECK["dag_check_connection — @hourly"]:::infra
    end

    subgraph ETL ["Pipeline Medallion — Airflow"]
        BRONZE["1_camada_bronze — @daily"]:::bronze
        SILVER["2_camada_silver — @daily"]:::silver
        GOLD["3_camada_gold — @daily"]:::gold
    end

    SETUP -.->|cria buckets e tabelas| BRONZE
    CHECK -.->|valida API e storage| BRONZE

    BRONZE --> DB_B[(bacen-lake/bronze)]
    DB_B --> SILVER
    SILVER --> DB_S[(bacen-lake/silver)]
    DB_S --> GOLD
    GOLD --> DB_G[(bacen-lake/gold)]

    subgraph STORAGE ["MinIO — Object Storage"]
        DB_B
        DB_S
        DB_G
    end

    DB_G -->|Delta Table| DASH([Streamlit Dashboard])

    classDef infra fill:#6c757d,color:#fff,stroke:none
    classDef bronze fill:#cd7f32,color:#fff,stroke:none
    classDef silver fill:#999,color:#fff,stroke:none
    classDef gold fill:#b8860b,color:#fff,stroke:none
```

---

## 📂 Estrutura do Repositório

A organização do projeto separa a **orquestração (DAGs)** da **lógica de processamento (Módulos)**, facilitando a manutenção e testes isolados:

```plaintext
├── dags/                      # Orquestração (Airflow)
│   ├── dag_bronze_ingest.py   # Extração API → Bronze
│   ├── dag_silver_transform.py# Transformação Bronze → Silver
│   ├── dag_gold_analytics.py  # Indicadores Silver → Gold
│   ├── dag_setup_db.py        # Inicialização de infraestrutura
│   ├── dag_check_connection.py # Monitoramento de serviços
│   └── lakehouse_dag.py       # DAG unificada (brazilian_economic_lakehouse)
├── src/                       # Módulos Core (Injetados em /dags/src/)
│   ├── api_client.py          # Cliente REST para o BACEN
│   ├── db_manager.py          # Conexão S3/MinIO e gestão de buckets
│   ├── delta_manager.py       # Operações ACID com Delta Lake
│   ├── transform.py           # Limpeza e Padronização (Silver)
│   └── analytics.py           # Cálculos de Juro Real (Gold)
├── data/minio_data/           # Persistência física do Lake
├── notebooks/                 # Exploração e Visualização de dados
├── docker-compose.yml         # Configuração dos microsserviços
└── .env                       # Credenciais e Endpoints
```

---

## 🛠️ Stack Tecnológica

- **Orquestração:** Apache Airflow 2.7.1  
- **Storage:** MinIO (S3-Compatible Object Storage)  
- **Tabelas:** Delta Lake (via delta-rs) para transações ACID  
- **Processamento:** Python (Pandas & Boto3)  
- **Infraestrutura:** Docker & Docker Compose  

---

## 🚀 Como Executar

### 1️⃣ Inicialização

Suba a infraestrutura completa (Airflow, Postgres e MinIO):

```bash
docker compose up -d
```

> **Nota:** No primeiro boot, o Airflow instalará as dependências do `requirements.txt`.  
> Aguarde a mensagem **"Airflow is ready"** nos logs.

---

### 2️⃣ Acesso e Credenciais

- **Airflow:** http://localhost:8080  
  - User: `admin`  
  - Senha:
    ```bash
    docker exec -it airflow_app cat standalone_admin_password.txt
    ```

- **MinIO:** http://localhost:9001  
  - User: `admin`  
  - Pass: `password`

---

### 3️⃣ Execução do Fluxo

Ative e dispare a DAG:

```
brazilian_economic_lakehouse
```

Isso irá processar automaticamente todas as camadas (**Bronze → Silver → Gold**).

---

## ✨ Desenvolvido por

**Samuel Frizzone Cardoso**

