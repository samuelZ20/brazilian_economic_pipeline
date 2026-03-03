# 🏦 Brazilian Economic Indicators — Delta Lake Pipeline

Pipeline de dados **End-to-End** que extrai indicadores econômicos do **Banco Central do Brasil (BACEN)**, processa em camadas **Medallion** e armazena em um **Delta Lake local** utilizando **MinIO**.

---

## 🏗️ Arquitetura e Fluxo de Dados

O projeto utiliza o **Apache Airflow** para orquestrar o fluxo entre as camadas, garantindo a integridade dos dados através de transações **ACID** do Delta Lake.

### 🔹 Infraestrutura

- Configuração automática de buckets  
- Validação de conectividade via DAGs de setup  

### 🥉 Camada Bronze

- Ingestão de dados brutos da API **SGS do BACEN**

### 🥈 Camada Silver

- Limpeza  
- Padronização  
- Tipagem dos dados  

### 🥇 Camada Gold

- Cálculo de indicadores analíticos  
- Exemplo: **Juro Real mensal**

---

## 🛠️ Stack Tecnológica

- **Orquestração:** Apache Airflow 2.7.1  
- **Armazenamento:** MinIO (S3-Compatible Object Storage)  
- **Processamento:** Python (Pandas & Delta-rs)  
- **Análise:** DuckDB & Jupyter Notebooks  
- **Infraestrutura:** Docker & Docker Compose  

---

## 📂 Estrutura do Repositório

Conforme organizado no ambiente de desenvolvimento:

```plaintext
├── dags/                          # Orquestração (Airflow)
│   ├── dag_bronze_ingest.py        # ETL: API → Bronze
│   ├── dag_silver_transform.py     # ETL: Bronze → Silver
│   ├── dag_gold_analytics.py       # ETL: Silver → Gold
│   ├── dag_setup_db.py             # Inicialização de infraestrutura
│   ├── dag_check_connection.py     # Monitoramento de serviços
│   └── lakehouse_dag.py            # DAG unificada do pipeline
│
├── src/                           # Módulos de Lógica (Core)
│   ├── api_client.py               # Consumo da API BACEN
│   ├── db_manager.py               # Interface com MinIO/S3
│   ├── delta_manager.py            # Operações Delta Lake
│   ├── transform.py                # Regras de limpeza (Silver)
│   ├── analytics.py                # Métricas de negócio (Gold)
│   └── utils.py                    # Funções auxiliares
│
├── data/minio_data/                # Volume de persistência do MinIO
├── notebooks/                      # Exploração de dados e visualização
├── docker-compose.yml              # Configuração dos serviços Docker
└── .env                            # Variáveis de ambiente
```

---

## 🚀 Como Executar

### 1️⃣ Inicialização do Ambiente

Clone o repositório e suba os contêineres:

```bash
docker compose up -d
```

> **Nota:** O Airflow instalará automaticamente as dependências necessárias no boot via `_PIP_ADDITIONAL_REQUIREMENTS`.

---

### 2️⃣ Acesso aos Serviços

#### 🔹 Airflow UI

- URL: http://localhost:8080  
- Usuário: `admin`  

Para obter a senha:

```bash
docker exec -it airflow_app cat standalone_admin_password.txt
```

#### 🔹 MinIO Console

- URL: http://localhost:9001  
- Usuário: `admin`  
- Senha: `password`  

---

### 3️⃣ Execução do Pipeline

No Airflow, execute as DAGs na seguinte ordem para o primeiro processamento:

1. `dag_setup_db`  
2. `dag_check_connection`  
3. `lakehouse_dag`  

> Alternativamente, execute as DAGs de cada camada individualmente.
