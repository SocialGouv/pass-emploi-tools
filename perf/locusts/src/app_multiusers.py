import asyncio
import os
import sys
import uuid
from contextlib import suppress
from http import HTTPStatus

import gevent
import stresstest.events
from locust import (Events, FastHttpUser, HttpUser, LoadTestShape,
                    SequentialTaskSet, TaskSet, between, constant_throughput,
                    events, tag, task)


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
# --------------------------------------------

# -- live patching -------------------------------------------------------------------
# tick() is executed each second
# into locust.runner.shape_worker, gevent.sleep is runned with the parameter max(1.0)
# if you want to increase the wait before each loop, we need to patch gevent.sleep (used into shape_worker)...
gevent.sleep_orig = gevent.sleep
def sleep_faster(*args, **kwargs):
    return gevent.sleep_orig(0.500)
# ------------------------------------------------------------------------------------

class APILoadShape(LoadTestShape):

    def tick(self):

        # patch only here. otherwise all gevent in locust will be impacted
        gevent.sleep = sleep_faster

        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        # --------------------------------------
        # FT   : 10/s
        # Milo :  1/s
        #---------------------------------------

        # Spawn users for ProfileUser1
        if int(self.get_run_time() % 2) == 0:
            return (self.get_current_user_count() + 10 , 10, [ProfilUser1])

        # Spawn users for ProfileUser2
        else:
            return (self.get_current_user_count() + 1, 1, [ProfilUser2])

