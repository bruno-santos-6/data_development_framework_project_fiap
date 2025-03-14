import pyodbc
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import os

def load_to_sql():
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    
    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key
    )
    
    file_client = service_client.get_file_system_client("refined").get_file_client("dados_processados.csv")
    download = file_client.download_file()
    df = pd.read_csv(download.readall())
    
    conn = pyodbc.connect(os.getenv("SQL_CONNECTION_STRING"))
    cursor = conn.cursor()
    
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dados_inflacao')
        CREATE TABLE dados_inflacao (
            orgao NVARCHAR(255),
            categoria NVARCHAR(255),
            ano INT,
            mes INT,
            valor FLOAT
        )
    """)
    
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dados_inflacao (orgao, categoria, ano, mes, valor)
            VALUES (?, ?, ?, ?, ?)
        """, row['orgao'], row['categoria'], row['ano'], row['mes'], row['valor'])
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_to_sql()