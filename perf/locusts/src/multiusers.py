from locust import (
    FastHttpUser,
    HttpUser,
    LoadTestShape,
    TaskSet,
    SequentialTaskSet,
    constant_throughput,
    between,
    Events,
    events,
    task,
    tag
)

import os
import sys
import uuid
import asyncio
import gevent

from http import HTTPStatus
from contextlib import suppress

import stresstest.events


def HTTPStatusReason(http_code):
    with suppress(ValueError):
        status = HTTPStatus(http_code)
        return f"{status.phrase} ({status.description})"
    return None



# ---------------------------------------
#           Tasks 
# ---------------------------------------


# Base is used only for internal fonctions (not tasks)
# If you use @task, push your fonction into CommonTaskSet
class BaseTaskSet(TaskSet):

    def shoot(self, url, name=None, traceback=None):
        if name is None:
            name = url
        with self.client.get(url, catch_response=True, name=name) as response:
            print(f"[DEBUG] shoot {url}")
            if traceback is not None:
                traceback(response)
            return response

    # TODO
    # Maybe switch to Error 5xx for failure()
    # 5xx => LB can't reach the app
    # another error code like 4xx isn't really useful
    def traceback(self, response):
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            response.success()
        elif status_code == HTTPStatus.CREATED:
            response.success()
        elif status_code == HTTPStatus.TOO_MANY_REQUESTS:
            response.success()   # success to avoid limit rate error 
            # (TODO: check if still necessary, used for some endpoint with limit rate)
        elif status_code == 0:
            response.failure(f"Failure: No Data (aborted)")
        elif status_code >= 500:   # Bad Gateway or Gateway timeout
            response.failure(f"Failure: Cannot reach app : {HTTPStatusReason(status_code)} (HTTP Code {status_code})")
        else:
            response.failure(f"Failure: {HTTPStatusReason(status_code)} (HTTP Code {status_code}) (*)")


# Common is used only for common tasks between users profiles
class CommonTaskSet(TaskSet):

    @task
    def favori(self):
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
    def recherche(self):
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



# ---------------------------------------
#           Tasks 
#         (specific)
# ---------------------------------------

# Specific Task for User 1 (FT)
class TasksUser1(BaseTaskSet, CommonTaskSet):

    @task
    def detail(self):
        name = f"/jeunes/{self.client.user_id}"
        url  = f"/jeunes/{self.client.user_id}"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    def accueil(self):
        name = f"/jeunes/{self.client.user_id}/pole-emploi/accueil (+parameters)"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/accueil?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    def demarches(self):
        name = f"/v2/jeunes/{self.client.user_id}/home/demarches"
        url  = f"/v2/jeunes/{self.client.user_id}/home/demarches"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    def agenda(self):
        name = f"/v2/jeunes/{self.client.user_id}/home/agenda/pole-emploi (+parameters)"
        url  = f"/v2/jeunes/{self.client.user_id}/home/agenda/pole-emploi?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    def monsuivi(self):
        name = f"/jeunes/{self.client.user_id}/pole-emploi/mon-suivi (+parameters)"
        url  = f"/jeunes/{self.client.user_id}/pole-emploi/mon-suivi?dateDebut=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)



# Specific Task for User 2 (MILO)
class TasksUser2(BaseTaskSet, CommonTaskSet):

    @task
    def monsuivi(self):
        name = f"/jeunes/milo/{self.client.user_id}/mon-suivi (+parameters)"
        url  = f"/jeunes/milo/{self.client.user_id}/mon-suivi?dateDebut=2025-01-01&dateFin=2025-01-31"
        self.shoot(url=url, name=name, traceback=self.traceback)

    @task
    def accueil(self):
        name = f"/jeunes/{self.client.user_id}/milo/accueil (+parameters)"
        url  = f"/jeunes/{self.client.user_id}/milo/accueil?maintenant=2025-01-01"
        self.shoot(url=url, name=name, traceback=self.traceback)





# ---------------------------------------
#           Profils
# ---------------------------------------

# Define Profil for User 1 (FT)
class ProfilUser1(HttpUser):

    tasks = [TasksUser1]

    def on_start(self):
        self.client.user_id = os.getenv("USERID_1")
        self.client.token   = os.getenv("TOKEN_1")
        self.client.headers = {
            "Authorization": f"Bearer {self.client.token}"
        }
        self.client.headers["accept"] = "*/*"

# Definie Profil for User 2 (MILO)
class ProfilUser2(HttpUser):

    tasks = [TasksUser2]

    def on_start(self):
        self.client.user_id = os.getenv("USERID_2")
        self.client.token   = os.getenv("TOKEN_2")
        self.client.headers = {
            "Authorization": f"Bearer {self.client.token}"
        }
        self.client.headers["accept"] = "*/*"



# -------------------------------------------
#       LoadTestShape
#       increase number of users to reach 
#       a specific fail_ratio
# --------------------------------------------

class APILoadShape(LoadTestShape):

    """
    # large load average
    user_count_leap = 10
    user_spawn_rate = 10
    user_spawn_incr = 25
    """
    # small load average
    user_count_leap = 1
    user_spawn_rate = 1
    user_spawn_incr = 2

    # users class handler
    users_handlers = [ProfilUser1, ProfilUser2]


    def __init__(self):
        print("calculating user_spawn_rate")
        self.user_spawn_rate = self.user_count_leap * self.user_spawn_incr

    def tick(self):
        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] current spawn rate : {self.user_spawn_rate}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        ratio = 0
        if self.runner.stats.total.num_requests > 0:
            ratio = (self.runner.stats.total.num_failures / self.runner.stats.total.num_requests)

        user_count = self.get_current_user_count()

        # ---- decrease -------
        if ratio > 0.8:
            print(f"[tick] (warning) stats ratio > 0.8 : {ratio}")
            user_count -= (self.user_count_leap / 2)
            if user_count <= 0:
                user_count = 1
            return (user_count, self.user_spawn_rate, self.users_handlers)

        # ---- increase -------
        user_count += self.user_count_leap

        # request:
        # Milo : 1 à 2 users par secondes max
        # FT   : 10 par seconde
        return (user_count, self.user_spawn_rate, self.users_handlers)
