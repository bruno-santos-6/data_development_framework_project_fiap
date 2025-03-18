# Data Development Framework - Pipeline de Dados do Banco Central

[![Azure Compliance](https://img.shields.io/badge/Azure%20Security-ISO27001-green)](https://azure.microsoft.com)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Visão Geral
Pipeline de dados completo para coleta, processamento e armazenamento de dados do Banco Central do Brasil (BCB), utilizando:
- **Coleta:** API do BCB → Azure Data Lake Gen2 (raw)
- **Processamento:** JSON → CSV consolidado (Azure Data Lake Gen2 refined)
- **Carga:** CSV → Azure SQL Database


## Requisitos
### Ambiente Local
- Docker Desktop
- Python 3.9+
- Azure CLI
- kubectl

### Azure
- Conta com permissões para:
  - AKS
  - Data Lake Gen2
  - Azure SQL
  - Container Registry

## Setup Inicial
### 1. Configuração do Ambiente
```bash
# Copiar variáveis de ambiente
cp environments/dev.env.example environments/dev.env

# Preencher com credenciais reais:
AZURE_TENANT_ID=11dbbfe2-89b8-4549-be10-cec364e59551
AZURE_CLIENT_ID=3a4b5c6d-7e8f-9a0b-c1d2-e3f4a5b6c7d8
AZURE_CLIENT_SECRET=kLq7$9VxR!pZ3@bNvF8#sT4dQw2^Ym
```

### 2. Construção das Imagens
```
# Build das imagens
docker-compose build

# Ver imagens criadas
docker images | grep "azcontaineregistryfiap"
```
# Uso Local
### 1. Executar Pipeline Completo
```
# Subir containers
docker-compose up -d

# Ver logs
docker-compose logs -f ingestion
docker-compose logs -f transformation
docker-compose logs -f load
```

### 2. Validação dos Dados
```
# Verificar dados no Data Lake
docker-compose run --rm validation python scripts/data-validation.py

# Consultar dados no SQL
sqlcmd -S sql-fiap-prod.database.windows.net -U svc_data_engineer -P "P@ssw0rd2024!Azure$" -Q "SELECT TOP 5 * FROM dados_inflacao"
```

# Deploy em Produção
### 1. Criar Infraestrutura Azure
```
# Criar recursos
az deployment group create --template-file infrastructure/azure-resources.json --parameters clusterName=aks-fiap-prod storageAccountName=sadatalakeprod

# Configurar NSG
az network nsg rule create --resource-group mba-bruno --nsg-name aks-nsg --name Allow_AzureServices --access Allow --protocol Tcp --direction Inbound --priority 100 --source-address-prefixes AzureCloud --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 443 1433
```
### 2. Deploy no AKS
```
# Conectar ao cluster
az aks get-credentials --resource-group mba-bruno --name k8s-mba-data-development-framework-aks --admin

# Aplicar manifestos
kubectl apply -f infrastructure/aks-deployment.yml

# Ver pods
kubectl get pods -n data-development-framework -w
```

# Validação de Segurança
```
# Verificar segredos no AKS
kubectl get secrets -n data-development-framework

# Testar acesso restrito
az storage fs access show --file-system raw --path bcb/inflacao/inflacao_ipca_duraveis.json --account-name sadatalakeprod
```

# Testes de Carga

```
# Executar Locust
locust -f scripts/stress-test.py --host=http://localhost:8080

# Acessar dashboard em http://localhost:8089
```

# Estrutura do Projeto

```
data_development_framework_project_fiap/
├── .github/
│ └── workflows/
│ └── ci-cd-pipeline.yml
├── environments/
│ ├── dev.env
│ └── prod.env
├── infrastructure/
│ ├── aks-deployment.yml
│ ├── azure-resources.json
│ └── vm-setup.sh
├── scripts/
│ ├── data-validation.py
│ └── stress-test.py
└── src/
├── 1-ingestion/
│ ├── Dockerfile
│ ├── main.py
│ └── requirements.txt
├── 2-transform/
│ ├── Dockerfile
│ ├── main.py
│ └── requirements.txt
├── 3-load/
│ ├── Dockerfile
│ ├── load_sql.py
│ └── requirements.txt
├── build/
│ ├── azure-deploy.ps1
│ ├── build-images.ps1
│ ├── deploy-aks.ps1
│ └── README.md
└── docs/
├── 01-architecture.md
├── 02-setup-guide.md
├── 03-api-reference.md
└── 04-security.md
```
