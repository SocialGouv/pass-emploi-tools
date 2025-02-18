from stresstest.users import ProfilUser
from stresstest.tasks.ft import TasksUser_Overload_Highest


# Define Profil for User FT
class ProfilUser(ProfilUser):

    tasks = [
        TasksUser_Overload_Highest
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id    = self.getenv("USER_ID")
        self.user_token = self.getenv("USER_TOKEN")

