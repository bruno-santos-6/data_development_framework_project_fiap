param (
    [string]$resourceGroup = $env:RESOURCE_GROUP,
    [string]$location = "eastus",
    [string]$templateFile = "../infrastructure/azure-resources.json"
)

az group create --name $resourceGroup --location $location

az deployment group validate `
  --resource-group $resourceGroup `
  --template-file $templateFile

az deployment group create `
  --resource-group $resourceGroup `
  --template-file $templateFile `
  --parameters `
    clusterName="aks-fiap-prod" `
    storageAccountName="sadatalakeprod"

Write-Host "Recursos Azure criados em $resourceGroup" -ForegroundColor Green