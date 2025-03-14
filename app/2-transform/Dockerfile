FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY transformation.py .

ENV AZURE_STORAGE_ACCOUNT_NAME=your_account
ENV AZURE_STORAGE_ACCOUNT_KEY=your_key

CMD ["python", "transformation.py"]