import pygame
import random
from assets import asset_path

class Food:
    def __init__(self, snake_body):
        self.cell_size = 20
        self.position = self.relocate(snake_body) 
        self.food_image = pygame.image.load(asset_path("mug.png"))

    def draw(self, screen):
        screen.blit(self.food_image, self.position)
        #pygame.draw.rect(screen,(255, 0, 0), (self.position[0], self.position[1], self.cell_size, self.cell_size))

    def relocate(self, snake_body):
        while True:
            new_position = (random.randrange(20, 580, 20), random.randrange(20, 580, 20))
            if new_position not in snake_body:
                return new_position
    
    def restart(self, snake_body):
        self.__init__(snake_body)