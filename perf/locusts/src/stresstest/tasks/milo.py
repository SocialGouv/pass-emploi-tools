from locust import (TaskSet, tag, task)

from stresstest.tasks import BaseTaskSet


# Specific Task for User 2 (MILO)
class TasksUser(BaseTaskSet, TaskSet):

    @task
    @tag("milo")
    def monsuivi(self):
        name = f"/jeunes/milo/{self.client.user_id}/mon-suivi"
        url  = f"/jeunes/milo/{self.client.user_id}/mon-suivi?dateDebut=2025-01-01&dateFin=2025-01-31"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("milo")
    def accueil(self):
        name = f"/jeunes/{self.client.user_id}/milo/accueil"
        url  = f"/jeunes/{self.client.user_id}/milo/accueil?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)

