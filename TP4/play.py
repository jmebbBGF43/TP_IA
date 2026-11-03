from agent import Game, GameAgent
import gymnasium as gym
import argparse
from enum import Enum
import sys, os, pickle

def launch(args):
    env = Game.getEnv(args.game, show=True)

    state, info = env.reset()

    agent = None
    if args.ai:
        if not os.path.isfile('agent-'+str(args.game)+'.dump'):
            print('agent-'+str(args.game)+'.dump')
            sys.stderr.write('no agent avaiable for '+str(args.game)+'\n')
            sys.exit(1)
        with open('agent-'+str(args.game)+'.dump', 'rb') as file:
            agent = pickle.load(file)

    episode_over = False
    while not episode_over:
        if agent == None:
            action = env.action_space.sample()  # choose randomly an action
        else:
            action = agent.get_determinist_action(state)# choose action according to a learned policy
        state, reward, terminated, truncated, info = env.step(action)

        episode_over = terminated or truncated
    env.close()




parser = argparse.ArgumentParser(description='Launch a game.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-r','--random',
                    dest='rand', action='store_true',
                    help="choose randomly actions during the game [default]")
group.add_argument('-i','--ai',
                    dest="ai", action="store_true",
                    help="choose actions using an AI trained with Q-learning")

parser.add_argument('game', type=Game, choices=list(Game))
args = parser.parse_args()

launch(args)