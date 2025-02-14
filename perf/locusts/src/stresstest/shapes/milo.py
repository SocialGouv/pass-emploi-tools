from locust import LoadTestShape


#
#   LoadShape MILO
#   --------------
#   Increase the number of users,
#   Then it reachs the limit, it stays in this step
#


class APILoadShape(LoadTestShape):

    def tick(self):

        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        if self.get_current_user_count() > 10:
            return (self.get_current_user_count(), 0)

        return (self.get_current_user_count() + 1, 1)
