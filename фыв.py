import pygame
import numpy as np
from pettingzoo import AECEnv, ParallelEnv
from pettingzoo.utils import agent_selector


class MazeEnv(ParallelEnv):
    metadata = {'render.modes': ['human']}
    def __init__(self, num_agen=2, maze_size=10):
        super().__init__()
        self.num_age = 2
        self.maze_size = maze_size
        self.width = 500
        self.height = 500
        self.block_size = self.width // self.maze_size
        self.maze = None
        self.agent_positions = [(0, 0), (self.maze_size-1, self.maze_size-1)]
        self.agent_colors = [(0, 255, 0), (0, 0, 255)]
        self.action_space = dict(zip(range(num_agen), ['up', 'down', 'left', 'right']))
        self.observation_space = dict(zip(range(num_agen), [self._get_observation_space(agent_id) for agent_id in range(num_agen)]))

    def _get_observation_space(self, agent_id):
        return np.zeros((self.maze_size, self.maze_size, 3), dtype=np.uint8)

    def observe(self, agent_id):
        obs = np.zeros((self.maze_size, self.maze_size, 3), dtype=np.uint8)
        #obs[self.agent_positions[agent_id][0], self.agent_positions[agent_id][1]] = self.agent_colors[agent_id]
        for i in range(self.maze_size):
            for j in range(self.maze_size):
                if self.maze[i][j] == 1:
                    obs[i, j] = (255, 255, 255)
        return obs

    def reset(self):
        self.maze = np.random.choice([0, 1], size=(self.maze_size, self.maze_size), p=[0.7, 0.3])
        self.maze[0][0] = 0
        self.maze[self.maze_size-1][self.maze_size-1] = 0
        self.agent_positions = [(0, 0), (self.maze_size-1, self.maze_size-1)]
        return self.observe(None)

    def step(self, actions):
        rewards = dict(zip(range(self.num_age), [0 for _ in range(self.num_age)]))
        dones = dict(zip(range(self.num_age), [False for _ in range(self.num_age)]))
        for agent_id, action in actions.items():
            row, col = self.agent_positions[agent_id]
            if action == 'up' and row > 0 and self.maze[row - 1][col] == 0:
                row -= 1
            elif action == 'down' and row < self.maze_size - 1 and self.maze[row + 1][col] == 0:
                row += 1
            elif action == 'left' and col > 0 and self.maze[row][col - 1] == 0:
                col -= 1
            elif action == 'right' and col < self.maze_size - 1 and self.maze[row][col + 1] == 0:
                col += 1
            self.agent_positions[agent_id] = (row, col)

        for agent_id, (row, col) in enumerate(self.agent_positions):
            if row == self.maze_size - 1 and col == self.maze_size - 1:
                rewards[agent_id] = 1
                dones[agent_id] = True
            else:
                rewards[agent_id] = -0.1

        return self.observe(None), rewards, dones, {}

    def render(self, mode='human'):
        if mode == 'human':
            pygame.init()
            screen = pygame.display.set_mode((self.width, self.height))
            clock = pygame.time.Clock()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                for i in range(self.maze_size):
                    for j in range(self.maze_size):
                        if self.maze[i][j] == 1:
                            pygame.draw.rect(screen, (255, 255, 255), (
                            j * self.block_size, i * self.block_size, self.block_size, self.block_size))

                for agent_id, (row, col) in enumerate(self.agent_positions):
                    pygame.draw.circle(screen, self.agent_colors[agent_id],
                                       (int((col + 0.5) * self.block_size), int((row + 0.5) * self.block_size)),
                                       self.block_size // 2)

                pygame.display.flip()
                clock.tick(30)

        elif mode == 'rgb_array':
            obs = self.observe(None)
            surface = pygame.surfarray.make_surface(obs)
            return pygame.surfarray.array3d(surface)

    def close(self):
        pygame.quit()

env = MazeEnv(num_agen=2, maze_size=10)




obs = env.reset()

done = False
while not done:
    action = {i: (0, 1) for i in range(env.num_age)}
    obs, reward, done, info = env.step(action)
    env.render()

env.close()