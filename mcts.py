import time
import copy
from random import choice
from test.test_mcts_env import Environment


class MCTS:
    def __init__(
            self,
            env,
            max_time,
            max_actions,
    ):
        self.max_time = float(max_time)
        self.max_actions = max_actions  # max simulation steps
        self.env = Environment()
        self.states = []
        # sim_state_count and sim_reward store information for UCT nodes
        # each node is a state
        self.sim_state_counts = {}  # how many times the state has been visited
        self.sim_state_rewards = {}  # averaged rewards for each state
        self.visited_states = set()  # states in the current path

    def update(self, state):
        self.states.append(state)

    def select(self, state):
        step = 0
        while step < self.max_actions:
            legal_actions = self.env.legal_actions(state)
            # get action-next_state pairs from environment
            action_next_state_pairs = [(action, self.env.next_state(state, action)) for action in legal_actions]

            # if all action-next_state pairs on the tree, select one



    def expand(self):
        pass

    def search(self):
        states_copy = copy.deepcopy(self.states)
        state = states_copy[-1]

        legal_actions = self.env.legal_actions(state)  # get all legal actions

        # if there's no legal action or only one action, return it
        if not legal_actions:
            return
        if len(legal_actions):
            return legal_actions[0]

        # Selection in MCTS
        self.select(state)

        # Expansion in MCTS
        self.expand()





    def get_action(self):
        state = self.states[-1]
        legal_actions = self.env.legal_actions(state)

        # if there's no legal action or only one action, return
        if not legal_actions:
            return
        if len(legal_actions) == 1:
            return legal_actions[0]

        self.sim_state_counts = {}
        self.sim_state_rewards = {}
        simulation_count = 0

        begin_time = time.time()
        while time.time() - begin_time < self.max_time:
            env_copy = copy.deepcopy(self.env)  # env deep copy for simulation
            self.simulate(env_copy)  # each simulation expands one and one roll-out node in UCT
            simulation_count += 1

        print('total simulations = {}'.format(simulation_count))

        best_action = self.select_best_action()

        return best_action

    def simulate(self, env):
        states_copy = self.states[:]  # copy the states list
        state = states_copy[-1]  # get the current state
        visited_states = set()

        # start simulation
        expand = True  # expand the tree leaf one step
        rewards_accum = 0
        for sim_step in range(self.max_sims):
            legal_actions = env.legal_actions(state)

            action = choice(legal_actions)  # randomly choose an legal action

            state, reward, done = env.condense_step(state, action)  # take one step in the environment

            rewards_accum += reward  # accumulate rewards
            states_copy.append(state)

            if expand and state not in self.states:
                expand = False
                self.sim_state_counts[state] = 0
                self.sim_state_rewards[state] = 0

            visited_states.add(state)

            if done:
                break

        # back propagate through tree path
        for state in visited_states:
            if state not in self.states:
                continue
            self.sim_state_counts[state] += 1
            self.sim_state_rewards[state] += rewards_accum

    def select_best_action(self):
        averaged_reward, action = max(
            (self.sim_state_rewards.get((self.states, action), 0) / self.sim_state_counts.get((self.states, action), 1),
             action) for action in self.env.legal_actions(self.states[-1])
        )

        return action




