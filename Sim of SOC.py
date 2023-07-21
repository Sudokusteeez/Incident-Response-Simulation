import random
import simpy
import numpy as np

NUM_ANALYSTS = 2
AVG_INCIDENT_TIME = 5
INCIDENT_INTERVAL = 2
SIM_TIME = 120

incidents_resolved = 0

class IncidentResponseTeam:
    def __init__(self, env, num_analysts, incident_time):
        self.env = env
        self.analysts = simpy.Resource(env, num_analysts)
        self.incident_time = incident_time

    def resolve_incident(self, incident):
        random_time = max(1, np.random.normal(self.incident_time, 4))
        yield self.env.timeout(random_time)
        print(f"Incident {incident} resolved at {self.env.now:.2f}")

def incident_generator(env, name, response_team):
    global incidents_resolved
    print(f"Incident {name} reported at {env.now:.2f}!")
    with response_team.analysts.request() as request:
        yield request
        print(f"Incident {name} assigned to an analyst at {env.now:.2f}")
        yield env.process(response_team.resolve_incident(name))
        print(f"Incident {name} resolved at {env.now:.2f}")
        incidents_resolved += 1

def setup(env, num_analysts, incident_time, incident_interval):
    response_team = IncidentResponseTeam(env, num_analysts, incident_time)

    for i in range(1, 6):
        env.process(incident_generator(env, i, response_team))

    while True:
        yield env.timeout(random.randint(incident_interval - 1, incident_interval + 1))
        i += 1
        env.process(incident_generator(env, i, response_team))

print("Starting Incident Response Simulation")
env = simpy.Environment()
env.process(setup(env, NUM_ANALYSTS, AVG_INCIDENT_TIME, INCIDENT_INTERVAL))
env.run(until=SIM_TIME)

print("Incidents resolved:", incidents_resolved)