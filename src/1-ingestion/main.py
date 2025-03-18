# ------------------------------------ app\1-ingestion\ingestion.py ------------------------------------ 
import os
import requests
import json
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from tenacity import retry, wait_exponential, stop_after_attempt

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
FILE_SYSTEM_NAME = "raw"

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def get_azure_credentials():
    return ClientSecretCredential(
        tenant_id=AZURE_TENANT_ID,
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET
    )

def main():
    try:
        credential = get_azure_credentials()
        service_client = DataLakeServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            credential=credential
        )
        file_system_client = service_client.get_file_system_client(FILE_SYSTEM_NAME)

        endpoints = json.loads(os.getenv("BCB_API_ENDPOINTS"))

        for endpoint in endpoints:
            response = requests.get(f"{endpoint['sourceBaseURL']}/{endpoint['sourceRelativeURL']}")
            response.raise_for_status()

            file_client = file_system_client.get_file_client(f"{endpoint['sinkFolderPath']}/{endpoint['sinkFileName']}")
            file_client.upload_data(response.content, overwrite=True)
            print(f"✅ {endpoint['sinkFileName']} processado com sucesso")

    except Exception as e:
        print(f"❌ Erro na ingestão: {str(e)}")
        raise

if __name__ == "__main__":
    main()