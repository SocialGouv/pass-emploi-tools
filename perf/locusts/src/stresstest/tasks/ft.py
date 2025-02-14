from locust import (TaskSet, tag, task)

from stresstest.tasks import BaseTaskSet

import uuid


# -----------------------------
#  Specific Task for User FT
# -----------------------------

class TasksUser(BaseTaskSet, TaskSet):

    @task
    @tag("ft")
    def detail(self):
        name = f"/jeunes/{self.client.user_id}"
        url  = f"/jeunes/{self.client.user_id}"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def accueil(self):
        name = f"/jeunes/{self.client.user_id}/pole-emploi/accueil"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/accueil?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def demarches(self):
        name = f"/v2/jeunes/{self.client.user_id}/home/demarches"
        url  = f"/v2/jeunes/{self.client.user_id}/home/demarches"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def agenda(self):
        name = f"/v2/jeunes/{self.client.user_id}/home/agenda/pole-emploi"
        url  = f"/v2/jeunes/{self.client.user_id}/home/agenda/pole-emploi?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def monsuivi(self):
        name = f"/jeunes/{self.client.user_id}/pole-emploi/mon-suivi"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/mon-suivi?dateDebut=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)


class TasksUser_Extension(BaseTaskSet, TaskSet):

    @task
    @tag("ft")
    def favoris(self):
        name = f"/jeunes/:id/favoris/"
        url  = f"/jeunes/{self.client.user_id}/favoris"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def recherches(self):
        name = f"/jeunes/:id/recherches"
        url  = f"/jeunes/{self.client.user_id}/recherches?avecGeometrie=true"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def recherches_suggestions(self):
        name = f"/jeunes/:id/recherches/suggestions"
        url  = f"/jeunes/{self.client.user_id}/recherches/suggestions"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def pole_emploi_accueil(self):
        name = f"/jeunes/:id/pole-emploi/accueil"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/accueil?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def pole_emploi_cv(self):
        name = f"/jeunes/:id/pole-emploi/cv"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/cv"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    @tag("ft")
    def pole_emploi_idp_token(self):
        name = f"/jeunes/:id/pole-emploi/idp-token"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/idp-token"
        self.shoot(url=url, name=name, traceback=self.traceback)


class TasksUser_POST(BaseTaskSet, TaskSet):

    @task
    @tag("ft")
    @tag("milo")
    def favoris(self):
        name = f"/jeunes/{self.client.user_id}/favoris/offres-emploi"
        url  = f"/jeunes/{self.client.user_id}/favoris/offres-emploi"
        data = {
            "idOffre": str(uuid.uuid4()),
            "titre": "string",
            "typeContrat": "string",
            "nomEntreprise": "string",
            "localisation": {
                "nom": "string",
                "codePostal": "string",
                "commune": "string"
            },
            "alternance": True,
            "duree": "string",
            "origineNom": "string",
            "origineLogo": "string"
        }
        with self.client.post(url, json=data, catch_response=True, name=name) as response:
            self.traceback(response)

    @task
    @tag("ft")
    @tag("milo")
    def recherches(self):
        name = f"/jeunes/{self.client.user_id}/recherches/offres-emploi"
        url  = f"/jeunes/{self.client.user_id}/recherches/offres-emploi"
        data = {
            "titre": "string",
            "metier": "string",
            "localisation": "string",
            "criteres": {
                "q": "string",
                "departement": "string",
                "alternance": True,
                "experience": ["1"],
                "debutantAccepte": True,
                "contrat": ["CDI"],
                "duree": ["1"],
                "commune": "string",
                "rayon": 0
            }
        }
        with self.client.post(url, json=data, catch_response=True, name=name) as response:
            self.traceback(response)


