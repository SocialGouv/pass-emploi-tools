from locust import LoadTestShape
import gevent

#
#   LoadShape Flood
#   ------------
#   Increase the number of users as fast as possible
#   CAUTION with this shape...
#   to use it, just add to your locust command line :
#   locust -f yourapp.py,stresstest/shapes/flood.py
#


#-- tips : live patching -------------------------------------------------------------
# change ALL gevent.sleep
gevent.sleep_orig = gevent.sleep
def sleep_faster(*args, **kwargs):
    return gevent.sleep_orig(0.005)
gevent.sleep = sleep_faster
#-------------------------------------------------------------------------------------


class APILoadShape(LoadTestShape):

    def tick(self):

        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        return (self.get_current_user_count() + 1 , 1)

