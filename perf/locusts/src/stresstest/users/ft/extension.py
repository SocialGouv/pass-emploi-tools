from stresstest.users import ProfilUser
from stresstest.tasks.ft import (TasksUser, TasksUser_Extension, TasksUser_Overload, TasksUser_Overload_Highest, TasksUser_POST)
from stresstest.tasks.plateforme import (TasksUser as TasksUser_Platform)


class ProfilUser(ProfilUser):

    tasks = [
        TasksUser,
        TasksUser_Extension,
        # TasksUser_POST,
        # TasksUser_Overload,
        # TasksUser_Overload_Highest,  # ! USE WITH CAUTION !
        # TasksUser_Platform,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = self.getenv("USER_ID")
        self.user_token = self.getenv("USER_TOKEN")
