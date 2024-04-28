import gym
from tetrisgame import TetrisEnv
import numpy as np
import pygame

# Register the environment
gym.register(
    id='TetrisGame-v0',
    entry_point='tetrisgame:TetrisEnv', 
    kwargs={'board': None} 
)

board = array_zeros = np.zeros((21, 10))

env = gym.make('TetrisGame-v0',board=board)
obs = env.reset()
env.render()

done = False
i = 0
while not done:
    pygame.event.get()
    action = env.action_space.sample()  # Random action selection
    obs, reward, done, _ = env.step(action)
    env.render()
    print('Reward:', reward)
    print('Done:', done)
    i += 1

    pygame.time.wait(100)