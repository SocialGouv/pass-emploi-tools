# API Simulator

Lazy API simulator

(works only with userId '20a2133e-94b7-4ef0-a530-9e11d0a7d093')


## Installation API Simulator

```sh
pip install -r requirements.txt
uvicorn app:app --port 8080 --workers 10
```

## Configuration PassEmploi API

edit .environment and change this variables :
 
```sh
OIDC_ISSUER_API_URL=http://127.0.0.1:8080/api
OIDC_ISSUER_URL=http://127.0.0.1:8080/issuer
MILO_API_URL=http://127.0.0.1:8080/milo
MILO_WEB_URL=http://127.0.0.1:8080/milo/dossier
IMMERSION_API_URL=http://127.0.0.1:8080/immersion
JECLIQUEOUPAS_API_URL=http://127.0.0.1:8080/jecliqueoupas
POLE_EMPLOI_API_BASE_URL=http://127.0.0.1:8080/poleemploi
POLE_EMPLOI_LOGIN_URL=http://127.0.0.1:8080/poleemploi/login
CJE_API_URL=http://127.0.0.1:8080/cje
MATTERMOST_JOBS_WEBHOOK_URL=http://127.0.0.1:8080/mattermost
MONITORING_DASHBOARD_URL=http://127.0.0.1:8080/monitoring
ELASTIC_DUMP_URL=http://127.0.0.1:8080/elastic
DIAGORIENTE_API_URL=http://127.0.0.1:8080/diagoriente
MATOMO_SOCIALGOUV_URL=http://127.0.0.1:8080/matomo
```
