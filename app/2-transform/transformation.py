import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import os
from datetime import datetime
import json

def process_data():
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    
    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key
    )

    categoria_mapping = {
        'inflacao_ipca_duraveis': 'Inflacao (IPCA) - Duraveis',
        'inflacao_ipca_servicos': 'Inflacao (IPCA) - Servicos',
        'inflacao_ipca_comercializaveis': 'Inflacao (IPCA) - Comercializaveis',
        'inflacao_ipca_nao_comercializaveis': 'Inflacao (IPCA) - Nao comercializaveis',
        'inflacao_ipca_bens_nao_duraveis': 'Inflacao (IPCA) - Bens nao-duraveis',
        'inflacao_ipca_itens_livres': 'Inflacao (IPCA) - Itens livres',
        'inflacao_ipca_precos_monitorados_total': 'Inflacao (IPCA) - Precos monitorados - Total',
        'inflacao_ipca_indice_de_difusao': 'Inflacao (IPCA) - Indice de difusao',
        'inflacao_ipca_nucleo_dupla_ponderacao': 'Inflacao (IPCA) - Nucleo de dupla ponderacao',
        'inflacao_ipca_nucleo_exclusao_ex2': 'Inflacao (IPCA) - Nucleo por exclusao - ex2',
        'inflacao_ipca_nucleo_medias_aparadas_com_suavizacao': 'Inflacao (IPCA) - Nucleo medias aparadas com suavizacao',
        'inflacao_ipca_nucleo_medias_aparadas_sem_suavizacao': 'Inflacao (IPCA) - Nucleo medias aparadas sem suavizacao',
        'inflacao_ipca_nucleo_exclusao_sem_monitorados_alimentos_domicilio': 'Inflacao (IPCA) - Nucleo por exclusao - Sem monitorados e alimentos no domicilio'
    }

    file_system_client = service_client.get_file_system_client("raw")
    inflacao_paths = file_system_client.get_paths(path="bcb/inflacao")
    
    dataframes = []
    categorias_agrupadas_por_ano = [] 

    for path in inflacao_paths:
        try:
            file_client = file_system_client.get_file_client(path.name)
            download = file_client.download_file()
            content = download.readall()
            
            filename = path.name.split('/')[-1].split('.')[0]
            categoria = categoria_mapping.get(filename, filename)
            
            df = pd.read_json(content)
            df['categoria'] = categoria
            
            df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
            df.rename(columns={'data': 'data_hora'}, inplace=True)
            df['data_hora'] = df['data_hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            df['ano'] = pd.to_datetime(df['data_hora']).dt.year
            if categoria not in categorias_agrupadas_por_ano:
                df['mes'] = pd.to_datetime(df['data_hora']).dt.month
            
            df['valor'] = df['valor'].astype(float)
            
            dataframes.append(df)
        except Exception as e:
            print(f"Erro ao processar {path.name}: {str(e)}")

    try:
        cotacao_path = "bcb/cotacao/cotacao_dolar_comercial.json"
        file_client = file_system_client.get_file_client(cotacao_path)
        download = file_client.download_file()
        cotacao_data = json.loads(download.readall())

        cotacoes = []
        for entry in cotacao_data['value']:
            dt = datetime.strptime(entry['dataHoraCotacao'], '%Y-%m-%d %H:%M:%S.%f')
            
            if entry.get('cotacaoVenda'):
                cotacoes.append({
                    'data_hora': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'valor': entry['cotacaoVenda'],
                    'categoria': 'Cotacao Dolar Comercial Venda'
                })
            
            if entry.get('cotacaoCompra'):
                cotacoes.append({
                    'data_hora': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'valor': entry['cotacaoCompra'],
                    'categoria': 'Cotacao Dolar Comercial Compra'
                })

        if cotacoes:
            cotacao_df = pd.DataFrame(cotacoes)
            cotacao_df['ano'] = pd.to_datetime(cotacao_df['data_hora']).dt.year
            cotacao_df['mes'] = pd.to_datetime(cotacao_df['data_hora']).dt.month
            dataframes.append(cotacao_df)
    except Exception as e:
        print(f"Erro ao processar cotação do dólar: {str(e)}")

    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)
        final_df['orgao'] = "Banco Central do Brasil"
        
        final_df = final_df[['orgao', 'categoria', 'ano', 'mes', 'valor']]
        
        output = final_df.to_csv(index=False).encode()
        refined_client = service_client.get_file_system_client("refined")
        file_client = refined_client.create_file("dados_financeiros_serie.csv")
        file_client.append_data(output, 0, len(output))
        file_client.flush_data(len(output))
        print("Dados transformados salvos com sucesso!")
    else:
        print("Nenhum dado foi processado.")

if __name__ == "__main__":
    process_data()