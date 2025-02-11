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




###########################################
#
#           Testing
#
###########################################


class APIUser(HttpUser):

    def on_start(self):
        authorization_key = os.getenv("AUTHORIZATION_KEY_USER")
        self.client.headers = {
            "Authorization": f"Bearer {authorization_key}"
        }
        self.user_id = os.getenv("USER_ID")


    # ----------------------------------------------------------------------------------

    def shoot(self, url, name=None, traceback=None):
        if name is None:
            name = url
        with self.client.get(url, catch_response=True, name=name) as response:
            print(f"[DEBUG] shoot {url}")
            if traceback is not None:
                traceback(response)
            return response

    ##
    ##
    ##  TODO : Maybe switch to Error 5xx for failure()
    ##         5xx => LB can't reach the app
    ##         another error code like 4xx isn't not really useful
    ##
    def traceback(self, response):
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            response.success()
        elif status_code == 429:
            response.success()
        elif status_code == 0:
            response.failure(f"Failure: No Data (aborted)")
        elif status_code >= 500:   # Bad Gateway or Gateway timeout
            response.failure(f"Failure: Cannot reach app : {HTTPStatusReason(status_code)} (HTTP Code {status_code})")
        else:
            response.failure(f"Failure: {HTTPStatusReason(status_code)} (HTTP Code {status_code}) (*)")

    # ----------------------------------------------------------------------------------

    # ------------------------------------------------------------------
    # GET directly the load balancer endpoint 
    # Reason: to check if LB is available
    # ------------------------------------------------------------------
    @task
    def loadbalancer(self):

        # because lb returns 404 by default
        def traceback(response):
            if response.status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
                response.failure(f"Failure : {response.status_code})")
            else:
                response.success()

        url = os.getenv("LOAD_BALANCER", self.host)
        self.shoot(url=url, name="Load Balancer", traceback=traceback)

    # ------------------------------------------------------------------
    # GET /health
    # Reason: compare if app is available (or down)
    # ------------------------------------------------------------------
    @task
    def health(self):
        self.shoot(url="/health", traceback=self.traceback)


    # -----------------------------------------------------------------
    # GET openid (simulator)
    # -----------------------------------------------------------------
    @task
    @tag("openid")
    def openid(self):
        url = "http://127.0.0.1:8080/issuer/protocol/openid-connect/token"
        with self.client.post(url, catch_response=True, name="openid (backbone)") as response:
            print(f"[DEBUG] shoot {url}")
            self.traceback(response)
            return response

    """
    # ------------------------------------------------------------------
    # GET /jeunes/:id/milo/accueil
    # Reason: lot of data (but it uses external API)
    # ------------------------------------------------------------------
    @task
    def jeunes_accueil(self):
        test_name = "/jeunes/:id/milo/accueil"
        date = "2025-01-01"
        url  = f"/jeunes/{self.user_id}/milo/accueil?maintenant={date}"
        self.shoot(url=url, name=test_name, traceback=self.traceback)
    """

    # ------------------------------------------------------------------
    # GET /jeunes/:idJeune
    # ------------------------------------------------------------------
    @task
    @tag("noapi")
    def jeunes_detail(self):
        test_name = "/jeunes (detail)"
        url  = f"/jeunes/{self.user_id}"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # ------------------------------------------------------------------
    # GET /jeunes/:idJeune/favoris
    # ------------------------------------------------------------------
    @task
    def jeunes_favoris(self):
        test_name = "/jeunes/:id/favoris/"
        url  = f"/jeunes/{self.user_id}/favoris"
        response = self.shoot(url=url, name=test_name, traceback=self.traceback)
        print(url, len(response.json()))

    # ------------------------------------------------------------------
    # GET /jeunes/:idJeune/recherches?avecGeometrie=true
    # ------------------------------------------------------------------
    @task
    def jeunes_recherches(self):
        test_name = "/jeunes/:id/recherches"
        url  = f"/jeunes/{self.user_id}/recherches?avecGeometrie=true"
        response = self.shoot(url=url, name=test_name, traceback=self.traceback)
        print(url, len(response.json()))

    # --------------------------------------------------------------------
    # GET /v2/jeunes/:idJeune/home/agenda/pole-emploi
    # TODO : RateLimit
    # OK        = 200
    # RateLimit = 429
    # --------------------------------------------------------------------
    @task
    @tag("startup")
    def jeunes_agenda_poleemploi(self):
        test_name = "/jeunes/:id/home/agenda/pole-emploi"
        url = f"/v2/jeunes/{self.user_id}/home/agenda/pole-emploi?maintenant=2025-01-01"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # --------------------------------------------------
    # GET /jeunes/:idJeune/conseillers
    # ==> CONSEILLER ONLY <==
    # TODO : BACKPORT TO ADMIN CLASS
    # --------------------------------------------------
    @task
    def jeunes_conseillers(self):
        test_name = "/jeunes/:id/conseillers"
        url = f"/jeunes/{self.user_id}/conseillers"

        authorization_key = os.getenv("AUTHORIZATION_KEY_ADMIN")
        self.client.headers = {"Authorization" : authorization_key}

        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # --------------------------------------------------
    # GET /jeunes/:idJeune/recherches/suggestions
    # --------------------------------------------------
    @task
    def jeunes_recherches_suggestions(self):
        test_name = "/jeunes/:id/recherches/suggestions"
        url = f"/jeunes/{self.user_id}/recherches/suggestions"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # -----------------------------------------------
    # GET /jeunes/:idJeune/pole-emploi/accueil
    # TODO : RateLimit
    # OK        = 200
    # RateLimit = 429
    # -----------------------------------------------
    @task
    @tag("startup")
    @tag("one")
    def jeunes_pole_emploi_accueil(self):
        test_name = "/jeunes/:id/pole-emploi/accueil"
        url = f"/jeunes/{self.user_id}/pole-emploi/accueil?maintenant=2025-01-01"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # -----------------------------------------------
    # GET /jeunes/:idJeune/pole-emploi/mon-suivi
    # TODO : RateLimit
    # OK        = 200
    # RateLimit = 429
    # -----------------------------------------------
    @task
    @tag("startup")
    def jeunes_pole_emploi_mon_suivi(self):
        test_name = "/jeunes/:id/pole-emploi/mon-suivi"
        url = f"/jeunes/{self.user_id}/pole-emploi/mon-suivi?dateDebut=2025-01-01"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # -----------------------------------------------
    # GET /jeunes/:idJeune/pole-emploi/cv
    # TODO : RateLimit
    # OK        = 200
    # RateLimit = 429
    # -----------------------------------------------
    @task
    def jeunes_pole_emploi_mon_suivi(self):
        test_name = "/jeunes/:id/pole-emploi/cv"
        url = f"/jeunes/{self.user_id}/pole-emploi/cv"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # ---------------------------------------------------
    # GET /v2/jeunes/:idJeune/home/demarches
    # ---------------------------------------------------
    @task
    @tag("startup")
    def jeunes_home_demarches(self):
        test_name = "/v2/jeunes/:id/home/demarches"
        url = f"/v2/jeunes/{self.user_id}/home/demarches"
        self.shoot(url=url, name=test_name, traceback=self.traceback)

    # ----------------------------------------------------
    # GET /referentiels/pole-emploi/catalogue-demarches
    # TODO : 200  => b'[]'   (erreur dans le serveur : "Impossible de récupérer le catalogue de démarches depuis PE")
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # GET /referentiels/pole-emploi/types-demarches
    # TODO : Fait appel à une API externe (entreprise.pe-qvr.fr)
    # ----------------------------------------------------
    @task
    def referentiels_catalogue_demarches(self):
        url = "/referentiels/pole-emploi/types-demarches?recherche=tout"
        self.shoot(url=url, traceback=self.traceback)


    # --------------------------------------------------------------
    # GET /jeunes/:id/pole-emploi/idp-token
    # --------------------------------------------------------------
    @task
    @tag("startup")
    def jeunes_pole_emploi_idp_token(self):
        test_name = "/jeunes/:id/pole-emploi/idp-token"
        url = f"/jeunes/{self.user_id}/pole-emploi/idp-token"
        self.shoot(url=url, name=test_name, traceback=self.traceback)






##############################################################
#
#       LoadTestShape
#  increase number of users to reach a specific fail_ratio
#
##############################################################


class APILoadShape(LoadTestShape):

    """
    user_count_leap = 10
    user_spawn_rate = 10
    user_spawn_incr = 25
    """
    user_count_leap = 1
    user_spawn_rate = 1
    user_spawn_incr = 2


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

        # decrease load (quickly)
        if ratio > 0.8:
            print(f"[tick] (warning) stats ratio > 0.8 : {ratio}")
            user_count -= (self.user_count_leap / 2)
            if user_count <= 0:
                user_count = 1
            return (user_count, self.user_spawn_rate)

        # increase load (slowly)
        user_count += self.user_count_leap
        return (user_count, self.user_spawn_rate)
