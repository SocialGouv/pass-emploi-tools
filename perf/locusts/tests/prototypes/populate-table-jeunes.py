import os
import sys
import uuid
import asyncio
import gevent
import requests


"""""""""

    Move to httpx and async

"""""""""

def create_jeune(self):
    # ----------------------------------------------------------------------
    # POST /conseillers/pole-emploi/jeunes
    #   input :
    #       firstName, lastName, email, idConseiller(token)
    #   output:
    #       201: ok    : json( id, lastname, firstname, idConseiller )
    #       409: error : already exists
    # ----------------------------------------------------------------------
    authorization_key = os.getenv("AUTHORIZATION_KEY_ADMIN")
    self.client.headers = {"Authorization" : authorization_key}
    response = self.client.post("/conseillers/pole-emploi/jeunes", data={
        "firstName"     : "TEST",
        "lastName"      : "TEST",
        "email"         : f"email-test-{uuid.uuid4()}@internal.local",
        "idConseiller"  : "cbf8fb13-8438-4981-8bbd-d74fbfb71fda"
    })
    if response.status_code == 201:
        id_jeune = response.json().get("id")
        print(response.json())
        print(">>>", id_jeune)
    else:
        return None

def get_favoris_offres_emploi(self):
    # POST /jeunes/:id/favoris/offres-emploi
    data = {
        "idOffre"       : "12345",
        "titre"         : "titre",
        "typeContrat"   : "typeContrat",
        "nomEntreprise" : "nomEntreprise",
        "localisation"  : {
            "nom"       : "localisationNom",
            "codePostal": "localisationcodePostal",
            "commune"   : "localisationCommune"
        },
        "alternance"    : True,
        "duree"         : "123",
        "origineNom"    : "origineNom",
        "origineLogo"   : "origineLogo"
    }
    response = self.client.post(f"/jeunes/{id_jeune}/favoris/offres-emploi", data=data)
    print(response.status_code)
    print(response.json())


