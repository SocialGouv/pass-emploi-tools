from locust import LoadTestShape
from stresstest.users.multiple import (ProfilUserFT, ProfilUserMILO)
import gevent


#-- live patching -------------------------------------------------------------------
# tick() is executed each second
# into locust.runner.shape_worker, gevent.sleep is runned with the parameter max(1.0)
# if you want to increase the wait before each loop, we need to patch gevent.sleep 
# (used into shape_worker)
#------------------------------------------------------------------------------------
gevent.sleep_orig = gevent.sleep
def sleep_faster(*args, **kwargs):
    return gevent.sleep_orig(0.500)
#------------------------------------------------------------------------------------


class APILoadShape(LoadTestShape):

    def tick(self):

        # patch only here. otherwise all gevent in locust will be impacted
        gevent.sleep = sleep_faster

        print(f"[tick] current user count : {self.get_current_user_count()}")
        print(f"[tick] stats num requests : {self.runner.stats.total.num_requests}")
        print(f"[tick] stats num failures : {self.runner.stats.total.num_failures}")

        # --------------------------------------
        # FT   : 10/s
        # Milo :  1/s
        #---------------------------------------

        # Spawn users for ProfileUser FT
        if int(self.get_run_time() % 2) == 0:
            return (self.get_current_user_count() + 10 , 10, [ProfilUserFT])

        # Spawn users for ProfileUser MILO
        else:
            return (self.get_current_user_count() + 1, 1, [ProfilUserMILO])
