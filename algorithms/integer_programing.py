from pulp import LpMaximize, LpProblem, LpVariable
from itertools import count
import sys
import os
from pathlib import Path
link=Path(os.path.abspath(__file__))
link=link.parent.parent
link=os.path.join(link, "system_model")
sys.path.append(link)
import environment as env
from config import *
import torch
import random

env=env.BusEnv()
optimize=0
env.seed(123)
batch_size=2
n_actions=NUM_ACTION
n_observations=NUM_STATE
env.replay()
true_move=[]
def nested_loops(env,depth, max_depth):
    if depth == max_depth:
        break
    else:
        # Tiếp tục lặp ở mức độ sâu kế tiếp
        for i in range(20):
            next_state, reward, done= env.step(i)
            nested_loops(env,depth + 1, max_depth)

for i in range(40):
        reward={}
        state = env.reset()
        done = False
        for  
        
# Define states and actions
states = ['s1', 's2']
actions = ['a1', 'a2', 'a3']

# Define reward function (ví dụ)


# Create LP problem
problem = LpProblem("Reinforcement_Learning", LpMaximize)

# Define decision variables
x = LpVariable.dicts("Action", (states, actions), lowBound=0, upBound=1, cat='Continuous')

# Add constraints: sum of actions in each state equals 1
for s in states:
    problem += sum(x[s][a] for a in actions) == 1

# Add objective function (maximize reward)
problem += sum(rewards[s, a] * x[s][a] for s in states for a in actions)

# Solve the problem
problem.solve()

# Print the results
for s in states:
    print(f"State: {s}")
    for a in actions:
        print(f"Action {a}: {x[s][a].varValue}")