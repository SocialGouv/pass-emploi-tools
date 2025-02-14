from locust import LoadTestShape

#
#   LoadShape FT
#   ------------
#   Increase the number of users, 
#   Then it reachs the limit, it stays in this step
#


#-- tips : live patching -------------------------------------------------------------
# tick() is executed each second
# into locust.runner.shape_worker, gevent.sleep is runned with the parameter max(1.0)
# if you want to increase the wait before each loop, we need to patch gevent.sleep
# (used into shape_worker)
#-------------------------------------------------------------------------------------
# gevent.sleep_orig = gevent.sleep
# def sleep_faster(*args, **kwargs):
#    return gevent.sleep_orig(0.500)
# and add :
# def tick(self):
# ++ # patch only here. otherwise all gevent in locust will be impacted
# ++ gevent.sleep = sleep_faster
#-------------------------------------------------------------------------------------


class APILoadShape(LoadTestShape):

    def tick(self):

        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        if self.get_current_user_count() > 40:
            return (self.get_current_user_count(), 0)

        return (self.get_current_user_count() + 10 , 10)

