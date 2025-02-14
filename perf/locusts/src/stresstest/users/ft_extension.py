from stresstest.users import ProfilUser
from stresstest.tasks.ft import (TasksUser, TasksUser_Extension, TasksUser_POST)


class ProfilUser(ProfilUser):

    tasks = [
        TasksUser,
        TasksUser_POST,
        TasksUser_Extension,  # More !
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = self.getenv("USER_ID")
        self.user_token = self.getenv("USER_TOKEN")
