from stresstest.users import ProfilUser
from stresstest.tasks.milo import TasksUser
from stresstest.tasks.ft import TasksUser_POST


# Define Profil for User MILO
class ProfilUser(ProfilUser):

    tasks = [
        TasksUser,
        TasksUser_POST
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = self.getenv("USER_ID_MILO")
        self.user_token = self.getenv("USER_TOKEN_MILO")

