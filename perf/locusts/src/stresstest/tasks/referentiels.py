from locust import (TaskSet, tag, task)

from stresstest.tasks import BaseTaskSet

class TasksUser(BaseTaskSet, TaskSet):

    @task
    def referentiels_catalogue_demarches(self):
        url = "/referentiels/pole-emploi/catalogue-demarches"

        # API responses 200 but with empty data
        def traceback(response):
            if response.status_code == 200 and len(response.json()) > 0:
                response.success()
            else:
                response.failure("Empty Response : {response.json()}")

        self.shoot(url=url, traceback=traceback)

    @task
    def referentiels_catalogue_demarches(self):
        url = "/referentiels/pole-emploi/types-demarches?recherche=tout"
        self.shoot(url=url, traceback=self.traceback)

