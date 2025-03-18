# Guia de Configuração

## Pré-requisitos Azure
1. Criar Service Principal:
   ```bash
   az ad sp create-for-rbac \
     --name "data-pipeline-sp" \
     --role "Contributor" \
     --scopes "/subscriptions/075bacb9-59ee-438a-ba03-3eb9db5ee5d8/resourceGroups/mba-bruno"
    ```

2.  Configurar Storage Account:
- Nome: sadatalakeprod
- Hierarchical Namespace: Habilitado
- Contêineres: raw, refined

3. Configurar Azure SQL:
```
CREATE DATABASE analytics_prod
COLLATE Latin1_General_100_CI_AS_SC_UTF8
```

# Configuração Local
1. Variáveis de ambiente:
```
# Azure AD
AZURE_TENANT_ID="11dbbfe2-89b8-4549-be10-cec364e59551" 
AZURE_CLIENT_ID="a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6"
AZURE_CLIENT_SECRET="kLq7$9VxR!pZ3@bNvF8#sT4dQw2^Ym"      

# Azure Storage
STORAGE_ACCOUNT_NAME="sadatalakefiap"                   
AZURE_STORAGE_ACCOUNT_KEY="Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBAS3O4rdDk0t8Xu24x7VBrTlnFjZP278F4@"

# Banco de Dados
SQL_SERVER="srv-fiap.database.windows.net"       
SQL_DATABASE="db-fiap"                              
SQL_USER="admin-fiap@srv-fiap"                   
SQL_PASSWORD="jgvUH#$5h4r$#n5"                    

# Azure Container Registry
ACR_REGISTRY="azcontaineregistryfiap.azurecr.io"                   

# Configuração dos Endpoints do BCB
BCB_API_ENDPOINTS=[
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.10843/dados?formato=json",
        "sinkFileName": "inflacao_ipca_duraveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.10844/dados?formato=json",
        "sinkFileName": "inflacao_ipca_servicos.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4447/dados?formato=json",
        "sinkFileName": "inflacao_ipca_comercializaveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4448/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nao_comercializaveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.10841/dados?formato=json",
        "sinkFileName": "inflacao_ipca_bens_nao_duraveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.11428/dados?formato=json",
        "sinkFileName": "inflacao_ipca_itens_livres.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4449/dados?formato=json",
        "sinkFileName": "inflacao_ipca_precos_monitorados_total.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.21379/dados?formato=json",
        "sinkFileName": "inflacao_ipca_indice_de_difusao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.16122/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_dupla_ponderacao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.16121/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_exclusao_ex2.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4466/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_medias_aparadas_com_suavizacao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.11426/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_medias_aparadas_sem_suavizacao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.11427/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_exclusao_sem_monitorados_alimentos_domicilio.json",
        "sinkFolderPath": "bcb/inflacao"
    }
]
```
2. Execução local:
```
docker-compose up --build
```