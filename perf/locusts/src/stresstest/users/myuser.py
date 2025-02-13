from stresstest.users import ProfilUser
from stresstest.tasks.mytasks import MyTasks

class MyUser(ProfilUser):
    tasks = [MyTasks]
