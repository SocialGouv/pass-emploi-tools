import uvicorn
from fastapi import FastAPI

app = FastAPI()

#
# uvicorn api-simulator:app --port 8080 --workers 10 
#


##################################################
##
##                OPENID API
##
##################################################

@app.get("/issuer/.well-known/openid-configuration")
async def openid_config():
    return {
        "authorization_endpoint"     : "http://127.0.0.1:8080/auth/realms/pass-emploi/protocol/openid-connect/auth",
        "claims_parameter_supported" : False,
        "claims_supported"           : [
            "sub",
            "email",
            "userId",
            "userRoles",
            "userStructure",
            "userType",
            "family_name",
            "given_name",
            "preferred_username",
            "sid",
            "auth_time",
            "iss"
        ],
        "code_challenge_methods_supported" : ["S256","plain"],
        "end_session_endpoint"             : "http://127.0.0.1:8080/auth/realms/pass-emploi/protocol/openid-connect/logout",
        "grant_types_supported"            : [
            "implicit",
            "authorization_code",
            "refresh_token",
            "urn:ietf:params:oauth:grant-type:token-exchange"
        ],
        "issuer"    : "http://127.0.0.1:8080/auth/realms/pass-emploi",
        "jwks_uri"  : "http://127.0.0.1:8080/auth/realms/pass-emploi/protocol/openid-connect/certs",
        "authorization_response_iss_parameter_supported" : True,
        "response_modes_supported"                       : [
            "form_post",
            "fragment",
            "query"
        ],
        "response_types_supported" : [
            "code id_token",
            "code",
            "id_token",
            "none"
        ],
        "scopes_supported" : [
            "openid",
            "offline_access",
            "email",
            "profile"
        ],
        "subject_types_supported" : ["public"],
        "token_endpoint_auth_methods_supported" : [
            "client_secret_basic",
            "client_secret_jwt",
            "client_secret_post",
            "private_key_jwt",
            "none"
        ],
        "token_endpoint_auth_signing_alg_values_supported" : ["HS256","RS256","PS256","ES256","EdDSA"],
        "token_endpoint" : "http://127.0.0.1:8080/auth/realms/pass-emploi/protocol/openid-connect/token",
        "id_token_signing_alg_values_supported" : ["PS256","RS256"],
        "pushed_authorization_request_endpoint" : "http://127.0.0.1:8080/auth/realms/pass-emploi/protocol/openid-connect/ext/par/request",
        "request_parameter_supported" : False,
        "request_uri_parameter_supported" : False,
        "userinfo_endpoint" : "http://127.0.0.1:8080/auth/realms/pass-emploi/protocol/openid-connect/userinfo",
        "claim_types_supported":["normal"]
    }



"""
POST params:
grant_type     : 'client_credentials'
client_id      : 'client_id',
client_secret  : 'client_secret'
"""
@app.post("/issuer/protocol/openid-connect/token")
async def openid_token():
    return {
        "issued_token_type" : "urn:ietf:params:oauth:token-type:access_token",
        "access_token"      : "VRCMjKZqeIvFFytRmhXE8V_AXiw",        # don't worries, it's from testing user
        "token_type"        : "bearer",
        "expires_in"        : 1139,
        "scope"             : "individu cpmetiers demarches openid prdvl profile prestationDE api_peconnect-individuv1 portefeuillecompetences coordonnees api_peconnect-telecharger-cv-realisationv1 api_peconnect-coordonneesv1 api_peconnect-demarchesv1 api_peconnect-metiersrecherchesv1 api_peconnect-conseillersv1 api_peconnect-gerer-prestationsv1 api_peconnect-rendezvousagendav2 email demarchesW"
    }


# TODO
@app.delete('/issuer/accounts/idAuth')
async def openid_delete():
    return None


# ----------- preprod -------------
# @app.get("/auth/realms/pass-emploi/protocol/openid-connect/certs")
async def openid_certs_preprod():
    return {
        "keys" : [{
            "kty":"RSA",
            "use":"sig",
            "kid":"8xLSMPDVXLfdcfuwR2Gaib-m67KXh0t7sXuTe16zZ-0",
            "e":"AQAB",
            "n":"6BGtvONO4jUwmfXP2kkNuyLhvY8WP4z-Onll4pnZmEHHVaMC9LbP52pDTN2HQWEA9wd6kWxDkdaDTo3QA4fTZoi39iLNtUpbVDYIX3NwDUk5EuaUOKfCtMwwAYh6K3sYQCPV6O7kwkBOMD8EYOZYqllpNcVvAAFCo1PRxt5p9FLSFSZqlTsQ2E0zi-3Rr68lKVvunXmRZKXGeHsjC9M-0-Gn9dAXJXmsbT6X2AbOMr4U_O73XSfKzpHcweCSKeJnRyVyt0k0Mto6ILtlPVRj7ujBYfesLfZhWp_BJpk5Roov458WLEGWIAH7d0puYrr228rPrtC_inJCpiEssMyC4Q"
        },{
            "kty":"RSA",
            "use":"sig",
            "kid":"UFcQqDxYxd2GuzhzqpQjXkqFZLMCzjeM1qVtp7DV43c",
            "e":"AQAB",
            "n":"lAcQZKng6AUEfR80Kq1-dH1v1kTH3i8nVX-8jtZ1L6wGT_E8N5Q1KyYF5Q3JNP-mL8h8YxmOEZr41xwCrExBIZET1BPLfGbEDBBvAvWCC8vC2IFkOmkTI_wiGlyb5zPnLP8jW5YzZVsmKjhto5BiobbkuY2pvvFGC3sXDcJIS_bkdtx6Ot-NuNEIYLBOuNO5MFDAF8QhBBEtZAMrGvKrSHW-QYltv-tJBwXL_JaiEpjYHnEwmdVVfr9axYwMaZ89Y-x0MaHIRBS59antWyfVqlFqD9S5jfIeJfGZ30eUOj9xe4jwjYvUjXEq5UWi2o_eRMDcnNPG4ycWaqXHw5rTDQ"
        }]}

# ----------- prod -------------
@app.get("/auth/realms/pass-emploi/protocol/openid-connect/certs")
async def openid_certs_prod():
    return {"keys":[{
        "kty":"RSA",
        "use":"sig",
        "kid":"1wFmZYL-OtucWGMarFJGzlExAoWGORwPja0DaanvIgY",
        "e":"AQAB",
        "n":"2o51f5Wo5_yTw2mwrENS7BR3B9lmr0KJ3ZoW398yqXdkJotEEMZvY73AGL7nAei0rfDKSsOMoM0H14FqdfhBJxTdRNCW_EKWlup8HgNb1H6IPSqZ42GGdEJUTyAgbwwXhFGQkwK7yFKDhMN_xVarHN-6Bsi8jQuSRFxEVuFWIuRn7CVaFy7VBTFJ0auz_4afUSxTjt3CqpN2WtVWk-VIuSo4noFlz_wSlksC-Odqa8jClkT5cU1Q9bqQUEYsXmB2bgkl66x93QD-eNiapAJ7t_YpvDn8uNzbF2mE2dsSQUR3l_4PExJn2sp00oO-vLSF0CRkmBahNcQeEMjCzyLpCQ"
    },{
        "kty":"RSA",
        "use":"sig",
        "kid":"zQcHql-8M0Lang9_fbvEkIx32XAohzBV0ZC0VycIL3I",
        "e":"AQAB",
        "n":"yfGYradf076ZPwrpfNbu2MoEbtUSYEtuq3MuSrzyVbwah24OPZ0aHez4_ihvlP6SbUG5hnf4LF03AZP0JgTAzoGG0zehJdGrfC9eW_Xt5ULd5lre6qjcio9_MkMtMlS2py1o1Q9_cnqqXlmCJUP_II7HXBjSoEClc_Z4AQvUK2fY85j5DIFFqziLMCTviqdiwX4MOQ3Cw5c9qxlKvY8dLT1BndXiKHXl8MLscniGp2gQoWKbiOSfp_l3qtWcYFs8gy8GZm7EOx0SxoR_B2Vg48kBFSdxRMOJdCWMfit7xOl80gkIDiOM3DnTlOAcEe3c_Tm8Z5LINDd2vsQtEnSIPQ"
    }]}




##################################################
##
##                POLE EMPLOI API
##
##################################################

@app.post("/poleemploi/login")
async def poleemploi_login():
    return {}   # strange, when auth returns is empty, API returns a fake returns (see below)

@app.post("/poleemploi/rechercher-demarche/v1/solr/search/demarche")
async def poleemploi_search():
    return {"listeDemarches" : [
        {
            "codeCommentDemarche": 'C12.06',
            "codePourQuoiObjectifDemarche": 'P03',
            "codeQuoiTypeDemarche": 'Q12',
            "estUneAction": False,
            "libelleCommentDemarche": 'Par un autre moyen',
            "libellePourQuoiObjectifDemarche": 'Mes candidatures',
            "libelleQuoiTypeDemarche": "Recherche d'offres d'emploi ou d'entreprises"
        }
    ]}
@app.get("/poleemploi/peconnect-telecharger-cv-realisation/v1/piecesjointes")
async def poleemploi_pj():
    return []

@app.get("/poleemploi/peconnect-demarches/v1/demarches")
async def poleemploi_peconnect_demarches():
    return [{
        "code": 'P02',
        "libelle": 'Ma formation professionnelle',
        "typesDemarcheRetourEmploi": [
          {
            "type": 'TypeDemarcheRetourEmploiReferentielPartenaire',
            "code": 'Q06',
            "libelle": "Information sur un projet de formation ou de Validation des acquis de l'expérience",
            "moyensRetourEmploi": [
              {
                "type": 'MoyenRetourEmploiReferentielPartenaire',
                "code": 'C06.01',
                "libelle": "En participant à un atelier, une prestation, une réunion d'information",
                "droitCreation": False
              }
            ]
          }
        ]
      }
    ]

""" params = dateRecherche=2025-02-10 """
@app.get("/poleemploi/peconnect-gerer-prestations/v1/rendez-vous")
async def poleemploi_peconnect_rdv():
    return []

""" params = ?dateDebut=2025-02-10T13%3A43%3A37.941Z """
@app.get("/poleemploi/peconnect-rendezvousagenda/v2/listerendezvous")
async def poleemploi_peconnect_listerdv():
    return []





##################################################
##
##                ANTIVIRUS API
##
##################################################

@app.post("/jecliqueoupas/submit")
async def jecliqueoupas_submit():
    return { "uuid": '??????????', "status": True }

@app.get("/jecliqueoupas/results/id-analyse")
async def jecliqueoupas_result_id_analyse():
    return { "is_malware": False, "done": True }



##################################################
##
##              DIAGORIENTE API
##
##################################################

@app.post("/graphql")
async def diagoriente_graphl():
    return { "data": {} }


#################################################
##
##              ENGAGEMENT API
##              TODO: used ?
##              mocked https://api.api-engagement.beta.gouv
##
#################################################

@app.get("/v0/mission/search")
async def engagement_search():
    return { "hits": [{
        "id": "unId",
        "title": "unTitre",
        "startAt": "2022-02-17T10:00:00.000Z",
        "domain": "Informatique",
        "city": "paris"
    }]}



#################################################
##
##              IMMERSION API
##              mocked by https://api.api-immersion.beta.gouv.
##
#################################################

@app.get('/v2/search/siret/appellationCode')
async def immersion_search_siret():
    return {
        "data": {
          "rome": 'mon-rome',
          "siret": 'siret',
          "romeLabel": 'romeLabel',
          "name": 'name',
          "nafLabel": 'nafLabel',
          "address": { "city": 'city' },
          "voluntaryToImmersion": True,
          "appellations": [
            {
              "appellationCode": 'appellationCode',
              "appellationLabel": 'appellationCodeLabel'
            }
          ]
        },
        "status": 200,
        "statusText": 'OK',
        "request": '',
        "headers": '',
        "config": ''
      }

@app.get('/v2/search')
async def immersion_search():
    return {
        "data": [
          {
            "rome": 'mon-rome',
            "siret": 'siret',
            "romeLabel": 'romeLabel',
            "name": 'name',
            "nafLabel": 'nafLabel',
            "address": { "city": 'city' },
            "voluntaryToImmersion": True,
            "appellations": [
              {
                "appellationCode": 'appellationCode',
                "appellationLabel": 'appellationCodeLabel'
              }
            ]
          }
        ],
        "status": 200,
        "statusText": 'OK',
        "request": '',
        "headers": '',
        "config": ''
    }

@app.post('/v2/contact-establishment')
async def immersion_contact_establishment():
    return {}




if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        # debug=False,
        access_log=False
    )
