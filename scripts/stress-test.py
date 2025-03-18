# ------------------------------------ scripts\stress-test.py ------------------------------------ 
from locust import HttpUser, task, between
import os
import json

class PipelineUser(HttpUser):
    wait_time = between(0.5, 2)
    headers = {"Content-Type": "application/json"}

    @task(3)
    def test_ingestion(self):
        self.client.post(
            "/ingest",
            json={
                "sourceBaseURL": "https://api.bcb.gov.br",
                "sourceRelativeURL": "dados/serie/bcdata.sgs.10843/dados?formato=json"
            },
            headers=self.headers
        )

    @task(2)
    def test_transformation(self):
        self.client.get("/transform-status", headers=self.headers)

    @task(1)
    def test_load(self):
        self.client.get("/load-metrics", headers=self.headers)