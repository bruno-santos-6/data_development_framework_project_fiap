# ------------------------------------ scripts\data-validation.py ------------------------------------ 
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
import os
import pandas as pd

def validate_data():
    credential = ClientSecretCredential(
        tenant_id=os.getenv("AZURE_TENANT_ID"),
        client_id=os.getenv("AZURE_CLIENT_ID"),
        client_secret=os.getenv("AZURE_CLIENT_SECRET")
    )

    service_client = DataLakeServiceClient(
        account_url=f"https://{os.getenv('STORAGE_ACCOUNT_NAME')}.dfs.core.windows.net",
        credential=credential
    )

    raw_client = service_client.get_file_system_client("raw")
    raw_files = list(raw_client.get_paths("bcb/inflacao"))  
    print(f"✅ Total arquivos raw: {len(raw_files)}")
    
    if len(raw_files) < 12:
        raise ValueError(f"Quantidade insuficiente de arquivos raw: {len(raw_files)}")

    refined_client = service_client.get_file_system_client("refined")
    processed_file = refined_client.get_file_client("processed/dados_financeiros.csv")
    
    if not processed_file.exists():
        raise FileNotFoundError("Arquivo processado não encontrado no Data Lake")

    df = pd.read_csv(processed_file.download_file().readall())
    required_columns = {'orgao', 'categoria', 'ano', 'mes', 'valor'}
    if not required_columns.issubset(df.columns):
        raise AssertionError(f"Colunas faltantes: {required_columns - set(df.columns)}")

    print("✅ Validação concluída com sucesso")

if __name__ == "__main__":
    validate_data()