from locust import (TaskSet, tag, task)
from stresstest.tasks import BaseTaskSet

class MyTasks(BaseTaskSet, TaskSet):

    @task
    def helloworld(self):
        self.shoot(url="/", name="helloworld", traceback=self.traceback)
