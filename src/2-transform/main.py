#  ------------------------------------ app\2-transform\transformation.py ------------------------------------ 
import os
import json
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
from tenacity import retry, wait_exponential, stop_after_attempt

STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME", "sadatalakeprod")
FILE_SYSTEM_RAW = "raw"
FILE_SYSTEM_REFINED = "refined"

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def process_data():
    try:
        credential = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )

        service_client = DataLakeServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            credential=credential
        )

        if not service_client.file_system_exists(FILE_SYSTEM_RAW):
            raise ValueError(f"Container {FILE_SYSTEM_RAW} não existe")

        raw_client = service_client.get_file_system_client(FILE_SYSTEM_RAW)
        paths = raw_client.get_paths("bcb/inflacao/")
        
        dfs = []
        for path in paths:
            if path.name.endswith(".json"):
                file_client = raw_client.get_file_client(path.name)
                data = json.loads(file_client.download_file().readall())
                
                categoria = path.name.split("/")[-1].replace(".json", "")
                df = pd.DataFrame(data)
                df['categoria'] = categoria
                dfs.append(df)
        
        consolidated = pd.concat(dfs, ignore_index=True)
        consolidated['data'] = pd.to_datetime(consolidated['data'], format='%Y-%m')
        consolidated['ano'] = consolidated['data'].dt.year
        consolidated['mes'] = consolidated['data'].dt.month
        
        refined_client = service_client.get_file_system_client(FILE_SYSTEM_REFINED)
        refined_client.get_file_client("processed/dados_financeiros.csv").upload_data(
            consolidated.to_csv(index=False),
            overwrite=True
        )
        
        print(f"✅ Processamento concluído: {len(consolidated)} registros")

    except Exception as e:
        print(f"❌ Falha no processamento: {str(e)}")
        raise

if __name__ == "__main__":
    process_data()