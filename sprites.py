
import pygame


'''Определите героя'''
class Hero(pygame.sprite.Sprite):
    def __init__(self, imagepath, coordinate, block_size, border_size, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath)
        self.image = pygame.transform.scale(self.image, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * block_size + border_size[0], coordinate[1] * block_size + border_size[1]
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size
    '''движение'''
    def move(self, action, maze):
        blocks_list = maze.blocks_list
        if action == 1: #up
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[0]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] - 1
                return True
        elif action == 2: #down
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[1]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] + 1
                return True
        elif action == 3: #left
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[2]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] - 1
                return True
        elif action == 4: #right
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[3]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] + 1
                return True
        # else:
        #     raise ValueError('Unsupport direction %s in Hero.move...' % direction)
    '''Привязка к экрану'''
    def draw(self, screen):
        self.rect.left, self.rect.top = self.coordinate[0] * self.block_size + self.border_size[0], self.coordinate[1] * self.block_size + self.border_size[1]
        screen.blit(self.image, self.rect)