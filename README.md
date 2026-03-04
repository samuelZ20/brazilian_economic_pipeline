# 🏦 Brazilian Economic Indicators — Delta Lake Pipeline

Pipeline de dados **End-to-End** que extrai indicadores econômicos do Banco Central do Brasil (BACEN), processa através da arquitetura **Medallion** e armazena em um **Delta Lake** local utilizando **MinIO**.

---

# 🏗️ Arquitetura do Projeto

O fluxo segue uma orquestração rígida onde a infraestrutura é validada antes do processamento dos dados.

## 📌 Diagrama do Fluxo

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

# ⚙️ Orquestração (Apache Airflow)

A orquestração completa é realizada via **Airflow**, garantindo transações **ACID** e o cumprimento das dependências entre as camadas.

### 📊 Visualização do Pipeline (Graph View)

Abaixo, a evidência do fluxo unificado `brazilian_economic_lakehouse` operando com sucesso em todas as etapas:

- **Ingestão:** Coleta dinâmica de dados da API SGS.  
- **Transformação:** Limpeza e tipagem para a camada Silver.  
- **Analytics:** Geração de indicadores e persistência em formato Delta na camada Gold.

---

# 📊 Visualização de Dados (Streamlit)

A interface de visualização consome diretamente a **Camada Gold** no MinIO, permitindo uma análise interativa dos indicadores econômicos processados.

## 📈 Dashboard de Indicadores

O dashboard provê uma visão clara das taxas **SELIC** e **IPCA**, com filtros dinâmicos e métricas atualizadas.

- Interface responsiva conectada ao Delta Lake via `delta-rs`.

---

# 📂 Estrutura do Repositório

```plaintext
├── dags/                      # Orquestração (Airflow)
│   ├── dag_bronze_ingest.py   # Extração API → Bronze
│   ├── dag_silver_transform.py# Transformação Bronze → Silver
│   ├── dag_gold_analytics.py  # Indicadores Silver → Gold
│   ├── dag_setup_db.py        # Inicialização de infraestrutura
│   ├── dag_check_connection.py # Monitoramento de serviços
│   └── lakehouse_dag.py       # DAG unificada
├── src/                       # Módulos Core e Dashboard
│   ├── api_client.py          # Cliente REST para o BACEN
│   ├── db_manager.py          # Gestão S3/MinIO
│   ├── delta_manager.py       # Operações Delta Lake
│   ├── dashboard.py           # Interface Streamlit
│   └── analytics.py           # Cálculos de Juro Real
├── docker-compose.yml         # Configuração dos microsserviços
└── .env                       # Credenciais e Endpoints
```

---

# 🛠️ Stack Tecnológica

- **Orquestração:** Apache Airflow 2.7.1  
- **Storage:** MinIO (S3-Compatible)  
- **Tabelas:** Delta Lake (transações ACID)  
- **Visualização:** Streamlit & Plotly  
- **Infraestrutura:** Docker & Docker Compose  

---

# 🚀 Como Executar

## 1️⃣ Inicialização

Suba a infraestrutura completa:

```bash
docker compose up -d
```

### 🔗 Endpoints

- **Airflow:** http://localhost:8080  
- **MinIO:** http://localhost:9001  
- **Dashboard:** http://localhost:8501  

---

# ✨ Desenvolvido por

**Samuel Frizzone Cardoso**
