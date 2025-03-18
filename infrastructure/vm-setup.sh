# ------------------------------------ infrastructure\vm-setup.ps1 ------------------------------------ 

# Instalar Chocolatey (gerenciador de pacotes)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar dependências
choco install -y docker-desktop azure-cli kubernetes-cli jq

# Iniciar serviço do Docker
Start-Service Docker
Set-Service -Name Docker -StartupType Automatic

# Configurar credenciais do Azure
$azureUsername = "svc_data_engineer@fiap.com"
$azurePassword = ConvertTo-SecureString "P@ssw0rd2024!Azure$" -AsPlainText -Force
$psCred = New-Object System.Management.Automation.PSCredential($azureUsername, $azurePassword)
Connect-AzAccount -Credential $psCred -Tenant "11dbbfe2-89b8-4549-be10-cec364e59551"

# Login no Azure Container Registry
az acr login --name azcontaineregistryfiap.azurecr.io

# Configurar contexto do AKS
az aks get-credentials `
  --resource-group mba-bruno `
  --name k8s-mba-data-development-framework-aks `
  --admin

# Verificar instalação
docker --version
kubectl version --client
az --version

Write-Host "Configuração concluída com sucesso!" -ForegroundColor Green