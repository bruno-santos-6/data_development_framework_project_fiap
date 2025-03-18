param (
    [string]$resourceGroup = $env:RESOURCE_GROUP,
    [string]$aksCluster = $env:AKS_CLUSTER,
    [string]$namespace = "data-development-framework"
)

if (-not $resourceGroup -or -not $aksCluster) {
    throw "RESOURCE_GROUP ou AKS_CLUSTER não definidos no environments/prod.env"
}

az aks get-credentials --resource-group $resourceGroup --name $aksCluster --admin

kubectl create namespace $namespace --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -f ../infrastructure/aks-deployment.yml -n $namespace

kubectl get pods -n $namespace -w