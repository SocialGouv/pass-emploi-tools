from locust import HttpUser


class ProfilUser(HttpUser):

    user_id = None
    token   = None

    def on_start(self):
        self.client.user_id    = self.user_id
        self.client.user_token = self.user_token
        self.client.headers = {
            "Authorization": f"Bearer {self.client.user_token}"
        }
        self.client.headers["accept"] = "*/*"

