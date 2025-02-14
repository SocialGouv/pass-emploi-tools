from locust import FastHttpUser
from os import getenv

class ProfilUser(FastHttpUser):

    user_id    = None
    user_token = None

    def on_start(self):
        self.client.user_id    = self.user_id
        self.client.user_token = self.user_token
        self.client.headers = {
            "Authorization": f"Bearer {self.client.user_token}"
        }

    def getenv(self, key=None, defaultvalue=None):
        return getenv(key, defaultvalue)

