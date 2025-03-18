# Referência de Endpoints

## API BCB (Ingestão)
| Endpoint | Descrição | Frequência |
|----------|-----------|-----------|
| `dados/serie/bcdata.sgs.10843/dados` | IPCA - Duráveis | Mensal |
| `dados/serie/bcdata.sgs.10844/dados` | IPCA - Serviços | Mensal |
| `dados/serie/bcdata.sgs.4447/dados` | IPCA - Comercializáveis | Mensal |
| `dados/serie/bcdata.sgs.4448/dados` | IPCA - Não Comercializáveis | Mensal |
| `dados/serie/bcdata.sgs.10841/dados` | IPCA - Bens Não Duráveis | Mensal |

## Azure SQL (Load)
| Tabela | Schema | Chaves |
|--------|--------|--------|
| `dados_inflacao` | `dbo` | `data_hora` (PK) |
| `dados_cotacao` | `dbo` | `data_hora` (PK) |

---

### **docs/04-validation.md**
```markdown
# Validação de Dados

## Passos:
1. Executar validação:
   ```bash
   docker run --env-file environments/prod.env data-validation:latest
   ```
2. Verificar saída:
```
Total arquivos raw: 12
Total arquivos refined: 1
```
3. Consulta SQL:
```
SELECT TOP 10 * FROM dados_inflacao ORDER BY data_hora DESC
```

# Critérios:
- Completeness: 100% dos endpoints BCB devem ter dados no Data Lake
- Accuracy: Valores devem corresponder aos dados originais do BCB
- Timeliness: Dados devem ser processados em até 15 minutos