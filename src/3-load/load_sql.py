# ------------------------------------ app\3-load\load_sql.py ------------------------------------ 
import os
import pandas as pd
import pyodbc
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def load_to_sql():
    try:
        credential = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )

        service_client = DataLakeServiceClient(
            account_url=f"https://{os.getenv('STORAGE_ACCOUNT_NAME')}.dfs.core.windows.net",
            credential=credential
        )
        
        file_client = service_client.get_file_system_client("refined").get_file_client("processed/dados_financeiros.csv")
        df = pd.read_csv(file_client.download_file().readall())

        conn = pyodbc.connect(os.getenv("SQL_CONNECTION_STRING"))
        cursor = conn.cursor()

        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'dados_inflacao')
            CREATE TABLE dados_inflacao (
                orgao NVARCHAR(255),
                categoria NVARCHAR(255),
                ano INT,
                mes INT,
                valor FLOAT,
                data_hora DATETIME
            )
        """)
        conn.commit()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO dados_inflacao (orgao, categoria, ano, mes, valor, data_hora)
                VALUES (?, ?, ?, ?, ?, ?)
            """, 
            row['orgao'], 
            row['categoria'], 
            row['ano'], 
            row['mes'], 
            row['valor'],
            pd.to_datetime(row['data_hora']).strftime('%Y-%m-%d %H:%M:%S')
            )
        
        conn.commit()
        print(f"✅ {len(df)} registros carregados no SQL Server")

    except Exception as e:
        print(f"❌ Falha no carregamento: {str(e)}")
        raise
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    load_to_sql()