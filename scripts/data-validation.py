from azure.storage.filedatalake import DataLakeServiceClient
import os

def validate_data():
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    
    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key
    )

    # Verificar dados brutos
    raw_files = service_client.get_file_system_client("raw").get_paths()
    print(f"Total arquivos raw: {sum(1 for _ in raw_files)}")

    # Verificar dados processados
    refined_files = service_client.get_file_system_client("refined").get_paths()
    refined_count = sum(1 for _ in refined_files)
    print(f"Total arquivos refined: {refined_count}")

    if refined_count == 0:
        raise Exception("Validação falhou: Nenhum dado processado encontrado")

if __name__ == "__main__":
    validate_data()