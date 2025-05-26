from locust import HttpUser, task, between
import random

class MLServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def predict(self):
        payload = {
            "x": random.uniform(0, 10),
            "gender": random.choice(["male", "female"])
        }
        self.client.post("/predict", json=payload)
