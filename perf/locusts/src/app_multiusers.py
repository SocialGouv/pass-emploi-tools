import stresstest.events
from stresstest.shapes.multiple import APILoadShape
from stresstest.users.multiple import (ProfilUserFT, ProfilUserMILO)

# locust workflow :
# load all user class -> read tasks variable -> load tasks class
# load shape if necessary
# load event if necessary
