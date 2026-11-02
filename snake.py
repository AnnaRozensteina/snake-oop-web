
import pygame
from pathlib import Path
from assets import asset_path


class Snake:
    def __init__(self):
        self.cell_size = 20
        self.head_image = pygame.image.load(asset_path("Sammy_head.png"))
        self.main_segment = pygame.image.load(asset_path("main_segment.png"))
        self.tapered_segment = pygame.image.load(asset_path("tapered_segment.png"))
        self.tail_end = pygame.image.load(asset_path("tail_end.png"))

        

        # Each tuple represents one body segment.
        # The first segment is the head.
        self.body = [
            (300, 300),
            (280, 300),
            (260, 300),
            (240, 300),
            (220, 300)
        ]
        self.directions = [(20, 0)] * len(self.body)

        # Direction is measured in pixels per move.
        self.direction = (self.cell_size, 0)

        self.turn_queue = []

    def move(self, grow=False):
        old_directions = self.directions.copy()

        if self.turn_queue:
            self.direction = self.turn_queue.pop(0)

        # Get the current head position
        head_x, head_y = self.body[0]

        # Calculate the new head position
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Add the new head and remove the tail
        self.body.insert(0, new_head)

        if not grow:
            self.body.pop()

        if grow:
            self.directions = [self.direction] + old_directions
        else:
            self.directions = [self.direction] + old_directions[:-1]


    def draw(self, screen):
        # Drawing the head
        angle = self.get_rotation_angle(self.directions[0])
        head = pygame.transform.rotate(self.head_image, angle)
        screen.blit(head, self.body[0])
        # Drawing the tail
        tapered_angle = self.get_rotation_angle(self.directions[-2])
        tapered = pygame.transform.rotate(self.tapered_segment, tapered_angle)

        tail_angle = self.get_rotation_angle(self.directions[-1])
        tail = pygame.transform.rotate(self.tail_end, tail_angle)

        screen.blit(tapered, self.body[-2])
        screen.blit(tail, self.body[-1])

        # Drawing main segments depending on snake length
        for i, segment in enumerate(self.body[1:-2], start=1):
            segment_angle = self.get_rotation_angle(self.directions[i])
            section = pygame.transform.rotate(self.main_segment, segment_angle)
            screen.blit(section, segment)

        """
            pygame.draw.rect(
                screen,
                (255, 159, 208),
                (segment[0], segment[1],
                 self.cell_size, self.cell_size),
            )
        """    
            
        
    
    def change_direction(self, direction):
        if len(self.turn_queue) >= 3:
            return
        
        if not self.turn_queue:
            reverse_direction = (-self.direction[0], -self.direction[1])
        else:
            reverse_direction = (-self.turn_queue[-1][0], -self.turn_queue[-1][1])
        
        if direction == reverse_direction:
            return
        
        self.turn_queue.append(direction)

    def restart(self):
        self.__init__()

    def get_rotation_angle(self, direction):
        if direction == (20, 0):
            return 0
        elif direction == (0, 20):
            return -90
        elif direction == (-20, 0):
            return 180
        elif direction == (0, -20):
            return 90