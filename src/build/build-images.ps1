param (
    [string]$acrRegistry = $env:ACR_REGISTRY,
    [string]$imageTag = "1.0.0"
)

if (-not $acrRegistry) {
    throw "ACR_REGISTRY não definido. Configure no environments/prod.env"
}

docker build -t "$acrRegistry/ingestion:$imageTag" -f ../app/1-ingestion/Dockerfile ../app/1-ingestion
docker build -t "$acrRegistry/transformation:$imageTag" -f ../app/2-transform/Dockerfile ../app/2-transform
docker build -t "$acrRegistry/load-sql:$imageTag" -f ../app/3-load/Dockerfile ../app/3-load

az acr login --name $acrRegistry.Split('.')[0]

docker push "$acrRegistry/ingestion:$imageTag"
docker push "$acrRegistry/transformation:$imageTag"
docker push "$acrRegistry/load-sql:$imageTag"

Write-Host "Build concluído: $acrRegistry/*.azurecr.io:$imageTag" -ForegroundColor Green