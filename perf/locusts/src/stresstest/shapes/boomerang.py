from locust import LoadTestShape

#
#   LoadShape Boomerang
#   -------------------
#   Increase the numbers of users until we reach a fail ratio
#   Then we decrease the number of users to calm down the stresstest
#   The picture is like a boomerang shape :)
#

class APILoadShape(LoadTestShape):

    """
    user_count_leap = 10
    user_spawn_rate = 10
    user_spawn_incr = 25
    """
    user_count_leap = 1
    user_spawn_rate = 1
    user_spawn_incr = 2

    """
    time_limit = 20
    spawn_rate = 20
    """

    def __init__(self):
        print("calculating user_spawn_rate")
        self.user_spawn_rate = self.user_count_leap * self.user_spawn_incr

    def tick(self):
        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] current spawn rate : {self.user_spawn_rate}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        ratio = 0
        if self.runner.stats.total.num_requests > 0:
            ratio = (self.runner.stats.total.num_failures / self.runner.stats.total.num_requests)

        user_count = self.get_current_user_count()

        # decrease load (quickly)
        if ratio > 0.8:
            print(f"[tick] (warning) stats ratio > 0.8 : {ratio}")
            user_count -= (self.user_count_leap / 2)
            if user_count <= 0:
                user_count = 1
            return (user_count, self.user_spawn_rate)

        # increase load (slowly)
        user_count += self.user_count_leap
        return (user_count, self.user_spawn_rate)
