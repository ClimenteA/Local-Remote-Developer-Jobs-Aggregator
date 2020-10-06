import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(2, 7)

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)
    def view_item(self):
        for page_num in range(100):
            self.client.get(f"/rjobs/all/{page_num}", name="/all")
            time.sleep(1)
