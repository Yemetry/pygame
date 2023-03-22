
from gymnasium.spaces import Discrete, Box
from pettingzoo import AECEnv, ParallelEnv
from pettingzoo.utils import agent_selector
from sprites import *
from mazes import *
import numpy as np
import os
import sys

class MazeEnv(ParallelEnv):
    def __init__(self, players):

        HEROPICPATH = os.path.join(os.getcwd(), 'hero.png')
        self.players = players
        self.agent_name_mapping = {agent: i for i, agent in enumerate(players)}
        pygame.init()
        self.display = pygame.display.set_mode((800, 625))
        self.clock = None
        self.maze_size = (20, 20)
        self.block_size = 20
        self.border_size = (50, 50)
        self.maze = RandomMaze(self.maze_size, self.block_size, self.border_size)
        self.hero = Hero(HEROPICPATH, [0, 0], self.block_size, self.border_size)
        self.agents = list(range(len(self.players)))
        self.agent_selector = agent_selector(self.agents)

        self.action_spaces = {agent: Discrete(4) for agent in players}
        self.observation_spaces = {agent: Box(low=0, high=255, shape=(640, 640, 3), dtype=np.uint8) for agent in players}

    def observe(self, agent):
        surface = pygame.display.get_surface()
        imgdata = pygame.surfarray.array3d(surface)
        imgdata = np.swapaxes(imgdata, 0, 1)
        return imgdata

    def reset(self):
        pygame.init()
        pygame.display.set_caption("Maze")
        self.display = pygame.display.set_mode((self.border_size[0]*2 + self.maze_size[1]*self.block_size,
                                                 self.border_size[1]*2 + self.maze_size[0]*self.block_size))
        self.clock = pygame.time.Clock()
        self.maze = RandomMaze(self.maze_size, self.block_size, self.border_size)
        return self.observe(self.agent_selector.reset())

    def render(self, mode="human"):
        self.display.fill((255, 255, 255))
        self.maze.draw(self.display)
        self.hero.draw(self.display)
        pygame.display.flip()

        pygame.display.update()

    def close(self):
        pygame.quit()
        sys.exit()


    def seed(self, seed=None):
        random.seed(seed)

    # def step(self, action):
    #     agent = self.agent_selector.next()
    #     success = self.hero.move(action[agent], self.maze)  # move the hero
    #     done = False
    #     reward = 0
    #
    #     if not success:  # if the move was unsuccessful, reward -1
    #         reward = -1
    #     obs = self.observe(agent)
    #     return obs, reward, done, {}
    # def step(self, action):
    #     agent = self.agent_selector.next()
    #     maze = self.maze
    #     hero = self.hero
    #     hero.move(action[agent], maze)
    #     done = False
    #     reward = 0
    #     if (self.hero.coordinate[0] == self.maze_size[1] - 1) and (self.hero.coordinate[1] == self.maze_size.MAZESIZE[0] - 1):
    #         done = True
    #         reward = 1
    #     obs = self.observe(agent)
    #     return obs, reward, done, {}
    def step(self, action):
        agent = self.agent_selector.next()

        self.hero.move(action, self.maze)
        done = False
        reward = 0
        # while True:

        is_move = False
        if action == 1:
            self.hero.move(1, self.maze)
            # is_move = self.hero.move(1, self.maze)
        elif action == 2:
            self.hero.move(2, self.maze)
            # is_move = self.hero.move(2, self.maze)
        elif action == 3:
            self.hero.move(3, self.maze)
            # is_move = self.hero.move(3, self.maze)
        elif action == 4:
            self.hero.move(4, self.maze)
            # is_move = self.hero.move(4, self.maze)
            self.hero.draw(self.display)
            self.maze.draw(self.display)
            # self.num_steps += int(is_move)

            # if (self.hero.coordinate[0] == self.maze_size[1] - 1) and (self.hero.coordinate[1] == self.maze_size.MAZESIZE[0] - 1):
            #     done = True
            #     reward = 1
            #     break
        pygame.display.update()

        obs = self.observe(agent)
        return obs, reward, done, {}
env = MazeEnv(players=[1,2])


obs = env.reset()

done = False
while not done:
    action = {i: (0, 1) for i in range(2)}
    obs, reward, done, info = env.step(action)
    env.step(action)
    env.render()

env.close()

