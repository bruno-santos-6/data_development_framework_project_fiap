FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y g++ unixodbc-dev
RUN pip install pyodbc pandas azure-storage-file-datalake

COPY load_sql.py .

ENV SQL_CONNECTION_STRING="Driver={ODBC Driver 18 for SQL Server};Server=your_server;Database=your_db;Uid=your_user;Pwd=your_pwd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

CMD ["python", "load_sql.py"]