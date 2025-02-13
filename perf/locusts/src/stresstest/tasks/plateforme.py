from locust import (TaskSet, tag, task)

from stresstest.tasks import BaseTaskSet

class TasksUser(BaseTaskSet, TaskSet):

    @task
    def health(self):
        self.shoot(url="/health", traceback=self.traceback)

    @task
    def openid(self):
        url = "http://127.0.0.1:8080/issuer/protocol/openid-connect/token"
        with self.client.post(url, catch_response=True, name="openid (backbone)") as response:
            print(f"[DEBUG] shoot {url}")
            self.traceback(response)
