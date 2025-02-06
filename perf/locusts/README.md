# Locusts stresstests

note: the project directory has been named "locusts" because python doesn't allow the name "locust" and will be on conflict with the library named locust.



## Python binaries

```sh
apt install python3         # Python interpreter + librairies
apt install python3-pip     # Python Package Manager
```

## Python Project Management : uv

Documentation : https://docs.astral.sh/uv/getting-started/installation/

```sh
pip install uv
```

## Python Virtual Environment

init :

```sh
uv venv
```

activation (important !):

```sh
source .venv/bin/activate
```

## Installing dependencies

```sh
uv sync
```

sync uses pyproject.yml and his dependencies.


## Using locust

Prepare .env file :

```sh
cp docs/env.template .env
edit .env
source .env
```

### Using web UI

```sh
locust -f src/app.py --host http://127.0.0.1:5000/
```
and open a browser tab to http://0.0.0.0:8089/


### Using only terminal 

```sh
locust -f src/app.py --host http://127.0.0.1:5000/ --headless
```


