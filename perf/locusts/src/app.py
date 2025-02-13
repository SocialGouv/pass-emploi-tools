import stresstest.events
from stresstest.shapes.unique import APILoadShape
from stresstest.users.unique import ProfilUser

# locust workflow :
# load all user class -> read tasks variable -> load tasks class
# load shape if necessary
# load event if necessary
