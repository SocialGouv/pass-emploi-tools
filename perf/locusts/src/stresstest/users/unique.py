import os

from stresstest.users import ProfilUser
from stresstest.tasks.ft import (TasksUserFT, TasksUserFT_Extension, TasksUserFT_POST)


class ProfilUser(ProfilUser):

    tasks = [TasksUserFT, TasksUserFT_Extension, TasksUserFT_POST]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = os.getenv("USER_ID")
        self.user_token = os.getenv("USER_TOKEN")
