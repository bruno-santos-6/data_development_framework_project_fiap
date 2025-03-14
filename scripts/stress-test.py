from locust import HttpUser, task, between
import os

class PipelineUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def test_ingestion(self):
        self.client.post("/ingest", json={
            "sourceBaseURL": "https://api.bcb.gov.br",
            "sourceRelativeURL": "dados/serie/bcdata.sgs.10843/dados?formato=json"
        })

    @task(3)
    def test_query(self):
        self.client.get("/query?year=2023")