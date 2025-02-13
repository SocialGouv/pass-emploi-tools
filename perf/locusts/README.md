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

----



# How to create a new scenario

Locust is driven by the `User` classes (`HttpUser` or `FastHttpUser`).

Locust loads all of this User classes, and looks for tasks definitions, then starts all tasks defined.

## Create a new user profile

To create a new scenario, create a new user file :

```python
# edit stresstest/users/myuser.py

from stresstest.users import ProfilUser
from stresstest.tasks.mytasks import MyTasks

class MyUser(ProfilUser):
    tasks = [MyTasks]
```

Note: ProfilUser is a subset of HttpUser. 

`tasks` defines all tasks executed by locust for this user profile.

## Create a new tasks file

You need to create "MyTasks" :

```python
# edit stresstest/tasks/mytasks.py

from locust import (TaskSet, tag, task)
from stresstest.tasks import BaseTaskSet

class MyTasks(BaseTaskSet, TaskSet):

    @task
    def helloworld(self):
        self.shoot(url="/", name="helloworld", traceback=self.traceback)
```

Note: `BaseTaskSet` is optional, you only need `TaskSet`.
`BaseTaskSet` adds some helpers like `.shoot()` and `.traceback()`

Only with these, you can now create a main locustfile which includes all of this classes :

## Create main file

```python
# edit myapp.py
from stresstest.users.myuser import MyUser
```

## Launch your new locust tests :

```shell
locust -f myapp.py
locust.main: Starting Locust 2.32.8
locust.main: Starting web interface at http://0.0.0.0:8089
```

If you need a load manager (to manage the number of users), use one of the shapes stored into stresstest/shapes/ and include them into your main file : locust will load him automatically :

```python
# edit myapp.py
from stresstest.users.myuser import MyUser
from stresstest.shapes.unique import APILoadShape
```

 That's it. 

Take a look in the other files to find out how to append more features.
