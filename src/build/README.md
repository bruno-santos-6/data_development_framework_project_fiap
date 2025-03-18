# Build e Deploy do Pipeline

## Pré-requisitos
1. Azure CLI instalado
2. Docker Desktop configurado
3. kubectl configurado
4. Variáveis de ambiente definidas em `environments/prod.env`

## Comandos

### Construir imagens
```powershell
.\build-images.ps1 -acrRegistry azcontaineregistryfiap.azurecr.io -imageTag 1.0.0
```

# Deploy no AKS

```powershell
.\deploy-aks.ps1 -resourceGroup mba-bruno -aksCluster k8s-mba-data-development-framework-aks
```

# Criar recursos Azure

```powershell
.\azure-deploy.ps1 -resourceGroup mba-bruno -location eastus
```

# Fluxo de Trabalho

1. Execute azure-deploy.ps1 para criar AKS e Storage Account
2. Execute build-images.ps1 para construir e enviar imagens
3. Execute deploy-aks.ps1 para implantar no cluster
