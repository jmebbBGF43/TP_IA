from agent import Game, GameAgent
import gymnasium as gym
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import argparse, pickle, os


def learn(args):
    # hyperparameters
    learning_rate = 0.01
    start_epsilon = 1.0
    epsilon_decay = start_epsilon / (args.n_episodes / 2)  # reduce the exploration over time
    final_epsilon = 0.1

    if os.path.isfile('agent-'+str(args.game)+'.dump'):    
        # Continues learning of Q-values from the dump file
        with open('agent-'+str(args.game)+'.dump', 'rb') as file:
            agent = pickle.load(file)
            start_epsilon = 0.25
            agent.set_hyperparameters(
                learning_rate=learning_rate,
                initial_epsilon=start_epsilon,
                epsilon_decay=start_epsilon / (args.n_episodes / 2),
                final_epsilon=final_epsilon)
            env = agent.env
            print(len(agent.q_values))
    
    else:
        # New Agent
        env = Game.getEnv(args.game, show=False)
        env = gym.wrappers.RecordEpisodeStatistics(env, 1000000)
        agent = GameAgent(
            env=env,
            learning_rate=learning_rate,
            initial_epsilon=start_epsilon,
            epsilon_decay=epsilon_decay,
            final_epsilon=final_epsilon,
        )

    for episode in tqdm(range(args.n_episodes)):
        state, info = env.reset()
        done = False

        # play one episode
        while not done:
            action = agent.get_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)

            # update the agent
            agent.update_q_value(state, action, reward, next_state)
            
            # update if the environment is done and the current state
            done = terminated or truncated
            state = next_state

        agent.decay_epsilon()

    # dump object with Q values
    file = open('agent-'+str(args.game)+'.dump', 'wb')
    # pickle.dump(agent.q_values, file)
    pickle.dump(agent, file)
    file.close()

    return env


def showStats(args, env):
    # plot the results
    fig, axs = plt.subplots(ncols=2, figsize=(12, 5))

    # Sliding window for episode evaluation (needs to be less than episodes)
    episode_window = 8

    axs[0].set_title("Episode rewards")
    # env.return_queue: The cumulative rewards of the last ``deque_size``-many episodes
    reward_moving_average = (
        np.convolve(
            np.array(env.return_queue).flatten(), np.ones(episode_window), mode="valid"
        )
        / episode_window
    )
    axs[0].plot(range(len(reward_moving_average)), reward_moving_average)

    axs[1].set_title("Episode lengths")
    # env.length_queue: The lengths of the last ``deque_size``-many episodes
    length_moving_average = (
        np.convolve(
            np.array(env.length_queue).flatten(), np.ones(episode_window), mode="valid"
        )
        / episode_window
    )
    axs[1].plot(range(len(length_moving_average)), length_moving_average)
    plt.tight_layout()
    plt.savefig('agent-'+str(args.game)+'.png')
    plt.show()
    plt.close()


parser = argparse.ArgumentParser(description='Learn an agent to play using Q-learning.')

parser.add_argument('game', type=Game, choices=list(Game))
parser.add_argument('-n', '--n_episodes', nargs='?',
                    dest='n_episodes', type=int, default=100,
                    help='number of episodes for Q-training')

args = parser.parse_args()

env = learn(args)
showStats(args, env)