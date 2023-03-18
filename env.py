import functools
import sys
import gymnasium
import pygame
from gymnasium.spaces import Discrete
from sprites import *
from mazes import *
import cfg
from pettingzoo import ParallelEnv
from pettingzoo.utils import parallel_to_aec, wrappers

up = 1
down = 2
left = 3
right = 4
MOVES = ["up", "down", "left", "right"]
NUM_ITERS = 100
REWARD_MAP = {
    # (ROCK, ROCK): (0, 0),
    # (ROCK, PAPER): (-1, 1),
    # (ROCK, SCISSORS): (1, -1),
    # (PAPER, ROCK): (1, -1),
    # (PAPER, PAPER): (0, 0),
    # (PAPER, SCISSORS): (-1, 1),
    # (SCISSORS, ROCK): (-1, 1),
    # (SCISSORS, PAPER): (1, -1),
    # (SCISSORS, SCISSORS): (0, 0),
}


def env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


def raw_env(render_mode=None):
    """
    To support the AEC API, the raw_env() function just uses the from_parallel
    function to convert from a ParallelEnv to an AEC env
    """
    env = parallel_env(render_mode=render_mode)
    env = parallel_to_aec(env)
    return env


class parallel_env(ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "rps_v2"}

    def __init__(self, render_mode=None):
        """
        The init method takes in environment arguments and should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces
        These attributes should not be changed after initialization.
        """
        self.screen = pygame.display.set_mode(cfg.SCREENSIZE)
        self.clock = pygame.time.Clock()
        self.maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE)
        self.hero_now = Hero(cfg.HEROPICPATH, [0, 0], cfg.BLOCKSIZE, cfg.BORDERSIZE)
        self.num_steps = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath)
        self.image = pygame.transform.scale(self.image, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * block_size + border_size[0], coordinate[1] * block_size + \
                                        border_size[1]
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size
        self.possible_agents = ["player_" + str(r) for r in range(2)]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )
        self.render_mode = render_mode

    # this cache ensures that same space object is returned for the same agent
    # allows action space seeding to work as expected
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return Discrete(4)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Discrete(3)

    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        pygame.display.set_caption('Maze Game')
        font = pygame.font.SysFont('Consolas', 15)
        self.clock.tick(cfg.FPS)
        self.screen.fill((255, 255, 255))
        self.is_move = False
        self.num_steps += int(self.is_move)
        self.hero_now.draw(self.screen)
        self.maze_now.draw(self.screen)
        showText(self.screen, font, 'USEDSTEPS: %s' % self.num_steps, (255, 0, 0), (410, 10))
        showText(self.screen, font, 'S: your starting point    D: your destination', (255, 0, 0), (10, 600))
        # if (self.hero_now.coordinate[0] == cfg.MAZESIZE[1] - 1) and (self.hero_now.coordinate[1] == cfg.MAZESIZE[0] - 1):
        #     break
        pygame.display.update()



    def close(self):
        pygame.display.quit()
        pygame.quit()

    def reset(self, seed=None, return_info=False, options=None):
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.
        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.
        Returns the observations for each agent
        """
        # self.agents = self.possible_agents[:]
        # self.num_moves = 0
        # observations = {agent: NONE for agent in self.agents}
        #
        # if not return_info:
        #     return observations
        # else:
        #     infos = {agent: {} for agent in self.agents}
        #     return observations, infos
        #
        #     while True:






    def step(self, actions):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath)
        self.image = pygame.transform.scale(self.image, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * block_size + border_size[0], coordinate[1] * block_size + \
                                        border_size[1]
        self.coordinate = self.coordinate
        self.block_size = self.block_size
        self.border_size = self.border_size
        blocks_list = maze.blocks_list
        if actions == 1:  # up
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[0]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] - 1
                return True
        elif actions == 2:  # down
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[1]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] + 1
                return True
        elif actions == 3:  # left
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[2]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] - 1
                return True
        elif actions == 4:  # right
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[3]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] + 1
                return True







        # If a user passes in actions with no agents, then just return empty observations, etc.
        if not actions:
            self.agents = []
            return {}, {}, {}, {}, {}

        # rewards for all agents are placed in the rewards dictionary to be returned
        rewards = {}
        # rewards[self.agents[0]], rewards[self.agents[1]] = REWARD_MAP[
        #     (actions[self.agents[0]], actions[self.agents[1]])
        # ]

        terminations = {agent: False for agent in self.agents}

        self.num_moves += 1
        env_truncation = self.num_moves >= NUM_ITERS
        truncations = {agent: env_truncation for agent in self.agents}

        # current observation is just the other player's most recent action
        observations = {
            self.agents[i]: int(actions[self.agents[1 - i]])
            for i in range(len(self.agents))
        }

        # typically there won't be any information in the infos, but there must
        # still be an entry for each agent
        infos = {agent: {} for agent in self.agents}

        if env_truncation:
            self.agents = []

        if self.render_mode == "human":
            self.render()
        return observations, rewards, terminations, truncations, infos
env = parallel_env

for i in range (100):
    env.step(((1,2,3,4), (4,1,2,3), (2,4,3,1), (2,3,4,3)))

    env.render()
env.close