from stresstest.users import ProfilUser
from stresstest.tasks.ft import (TasksUserFT, TasksUserFT_POST)
from stresstest.tasks.milo import TasksUserMILO


# Define Profil for User FT
class ProfilUserFT(ProfilUser):

    tasks = [TasksUserFT, TasksUserFT_POST]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = self.getenv("USER_ID")
        self.user_token = self.getenv("USER_TOKEN")


# Define Profil for User MILO
class ProfilUserMILO(ProfilUser):

    tasks = [TasksUserMILO, TasksUserFT_POST]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = self.getenv("USER_ID_MILO")
        self.user_token = self.getenv("USER_TOKEN_MILO")

