import requests
import os
from azure.storage.filedatalake import DataLakeServiceClient

configs = [
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.10843/dados?formato=json",
        "sinkFileName": "inflacao_ipca_duraveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.10844/dados?formato=json",
        "sinkFileName": "inflacao_ipca_servicos.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4447/dados?formato=json",
        "sinkFileName": "inflacao_ipca_comercializaveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4448/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nao_comercializaveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.10841/dados?formato=json",
        "sinkFileName": "inflacao_ipca_bens_nao_duraveis.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.11428/dados?formato=json",
        "sinkFileName": "inflacao_ipca_itens_livres.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4449/dados?formato=json",
        "sinkFileName": "inflacao_ipca_precos_monitorados_total.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.21379/dados?formato=json",
        "sinkFileName": "inflacao_ipca_indice_de_difusao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.16122/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_dupla_ponderacao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.16121/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_exclusao_ex2.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.4466/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_medias_aparadas_com_suavizacao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.11426/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_medias_aparadas_sem_suavizacao.json",
        "sinkFolderPath": "bcb/inflacao"
    },
    {
        "sourceBaseURL": "https://api.bcb.gov.br",
        "sourceRelativeURL": "dados/serie/bcdata.sgs.11427/dados?formato=json",
        "sinkFileName": "inflacao_ipca_nucleo_exclusao_sem_monitorados_alimentos_domicilio.json",
        "sinkFolderPath": "bcb/inflacao"
    }
]

def upload_to_datalake(file_content, file_path):
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    
    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key
    )
    
    file_system_client = service_client.get_file_system_client("raw")
    directory_client = file_system_client.get_directory_client(os.path.dirname(file_path))
    
    if not directory_client.exists():
        directory_client.create_directory()
    
    file_client = directory_client.create_file(os.path.basename(file_path))
    file_client.append_data(file_content, 0, len(file_content))
    file_client.flush_data(len(file_content))

def main():
    for config in configs:
        try:
            url = f"{config['sourceBaseURL']}/{config['sourceRelativeURL']}"
            response = requests.get(url)
            response.raise_for_status()
            
            file_path = f"{config['sinkFolderPath']}/{config['sinkFileName']}"
            upload_to_datalake(response.content, file_path)
            print(f"Arquivo {file_path} carregado com sucesso")
        except Exception as e:
            print(f"Erro no processamento {config['sinkFileName']}: {str(e)}")

if __name__ == "__main__":
    main()