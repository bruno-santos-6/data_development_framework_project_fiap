#!/bin/bash

# Install required tools
sudo apt-get update
sudo apt-get install -y \
    docker.io \
    docker-compose \
    azure-cli \
    kubectl \
    jq

# Configure Docker permissions
sudo usermod -aG docker $USER
newgrp docker

# Login to Azure Container Registry
az acr login --name youracr

# Configure Kubernetes
az aks get-credentials \
    --resource-group your-resource-group \
    --name your-aks-cluster

echo "Setup completed successfully!"