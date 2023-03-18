
import pygame
import random


def showText(screen, font, text, color, position):
    text_render = font.render(text, True, color)
    rect = text_render.get_rect()
    rect.left, rect.top = position
    screen.blit(text_render, rect)
    return rect.right


'''Блок игровой карты'''
class Block():
    def __init__(self, coordinate, block_size, border_size, **kwargs):
        # (col, row)
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size
        self.is_visited = False
        # Есть ли стена сверху, снизу, слева и справа.
        self.has_walls = [True, True, True, True]
        self.color = (0, 0, 0)
    '''Рисование на экране'''
    def draw(self, screen):
        directions = ['top', 'bottom', 'left', 'right']
        for idx, direction in enumerate(directions):
            if self.has_walls[idx]:
                if direction == 'top':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = self.coordinate[1] * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'bottom':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'left':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'right':
                    x1 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
        return True


'''Случайно сгенерированные классы лабиринтов'''
class RandomMaze():
    def __init__(self, maze_size, block_size, border_size, **kwargs):
        self.block_size = block_size
        self.border_size = border_size
        self.maze_size = maze_size
        self.blocks_list = RandomMaze.createMaze(maze_size, block_size, border_size)
        self.font = pygame.font.SysFont('Consolas', 15)
    '''Картина на экране'''
    def draw(self, screen):
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                self.blocks_list[row][col].draw(screen)
        # Указатели старта и финиша
        showText(screen, self.font, 'S', (255, 0, 0), (self.border_size[0]-10, self.border_size[1]))
        showText(screen, self.font, 'D', (255, 0, 0), (self.border_size[0]+(self.maze_size[1]-1)*self.block_size, self.border_size[1]+self.maze_size[0]*self.block_size+5))
    '''Создание лабиринта'''
    @staticmethod
    def createMaze(maze_size, block_size, border_size):
        def nextBlock(block_now, blocks_list):
            directions = [1, 2, 3, 4]
            blocks_around = dict(zip(directions, [None]*4))
            block_next = None
            count = 0
            # Просмотр верхнего блока
            if block_now.coordinate[1]-1 >= 0:
                block_now_top = blocks_list[block_now.coordinate[1]-1][block_now.coordinate[0]]
                if not block_now_top.is_visited:
                    blocks_around[1] = block_now_top
                    count += 1
            # Посмотреть блок ниже
            if block_now.coordinate[1]+1 < maze_size[0]:
                block_now_bottom = blocks_list[block_now.coordinate[1]+1][block_now.coordinate[0]]
                if not block_now_bottom.is_visited:
                    blocks_around[2] = block_now_bottom
                    count += 1
            # Просмотр левого блока
            if block_now.coordinate[0]-1 >= 0:
                block_now_left = blocks_list[block_now.coordinate[1]][block_now.coordinate[0]-1]
                if not block_now_left.is_visited:
                    blocks_around[3] = block_now_left
                    count += 1
            # Просмотр правого блока
            if block_now.coordinate[0]+1 < maze_size[1]:
                block_now_right = blocks_list[block_now.coordinate[1]][block_now.coordinate[0]+1]
                if not block_now_right.is_visited:
                    blocks_around[4] = block_now_right
                    count += 1
            if count > 0:
                while True:
                    direction = random.choice(directions)
                    if blocks_around.get(direction):
                        block_next = blocks_around.get(direction)
                        if direction == 1:
                            block_next.has_walls[1] = False
                            block_now.has_walls[0] = False
                        elif direction == 2:
                            block_next.has_walls[0] = False
                            block_now.has_walls[1] = False
                        elif direction == 3:
                            block_next.has_walls[3] = False
                            block_now.has_walls[2] = False
                        elif direction == 4:
                            block_next.has_walls[2] = False
                            block_now.has_walls[3] = False
                        break
            return block_next
        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in range(maze_size[0])]
        block_now = blocks_list[0][0]
        records = []
        while True:
            if block_now:
                if not block_now.is_visited:
                    block_now.is_visited = True
                    records.append(block_now)
                block_now = nextBlock(block_now, blocks_list)
            else:
                block_now = records.pop()
                if len(records) == 0:
                    break
        return blocks_list