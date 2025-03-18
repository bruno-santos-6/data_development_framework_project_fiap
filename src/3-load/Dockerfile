#  ------------------------------------ app\3-load\Dockerfile ------------------------------------ 
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y unixodbc-dev  # Necessário para pyodbc
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/lib/x86_64-linux-gnu/libodbc* /usr/lib/x86_64-linux-gnu/
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "load_sql.py"]  # Corrigido nome do script