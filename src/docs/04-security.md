# Segurança

## Configurações Obrigatórias:
1. **Azure Key Vault:**
   ```bash
   az keyvault create --name kv-fiap-prod --resource-group mba-bruno
   az keyvault secret set --name sql-password --value "P@ssw0rd2024!Azure$"
    ```
2. Network Security Group:
```
{
  "name": "allow-azure-services",
  "properties": {
    "protocol": "TCP",
    "sourcePortRange": "*",
    "destinationPortRange": "1433",
    "sourceAddressPrefix": "AzureCloud",
    "access": "Allow"
  }
}
```
3. Azure Policy:
- Exigir HTTPS em todas as conexões
- Bloquear contas de armazenamento públicas

```
---

### **docs/08-troubleshooting.md**
```markdown
# Guia de Problemas Comuns

## Erro: `403 Forbidden` no Data Lake
**Causa:** Permissões insuficientes do Service Principal  
**Solução:**
```bash
az role assignment create \
  --assignee 3a4b5c6d-7e8f-9a0b-c1d2-e3f4a5b6c7d8 \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/075bacb9-59ee-438a-ba03-3eb9db5ee5d8/resourceGroups/mba-bruno/providers/Microsoft.Storage/storageAccounts/sadatalakeprod"
```

Erro: `Connection Timeout` no SQL
Causa: NSG bloqueando porta 1433
Solução: Permitir tráfego na porta 1433 para o IP do AKS

```
Erro: Connection Timeout no SQL
Causa: NSG bloqueando porta 1433
Solução: Permitir tráfego na porta 1433 para o IP do AKS
```