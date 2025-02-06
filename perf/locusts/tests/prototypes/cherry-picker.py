from app import APIUser

from locust.env import Environment
from locust import HttpUser, events, task

env = Environment(user_classes=[APIUser], events=events)
env.host = "http://127.0.0.1:5000"

runner = env.create_local_runner()

env.events.init.fire(environment=env, runner=runner, web_ui=None)

runner.start(1, spawn_rate=1)
runner.greenlet.join()
