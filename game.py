
import asyncio
import pygame

from snake import Snake
from food import Food


BACKGROUND = (25, 25, 25)
SCREEN_SIZE = (600, 600)
MOVE_INTERVAL = 200  # milliseconds between automatic moves


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Snake")

        self.snake = Snake()
        self.food = Food(self.snake.body)

        self.running = True
        self.game_over = False
        self.score = 0

        self.font = pygame.font.SysFont("Courier New", 30)
        self.font_game_over = pygame.font.SysFont("Courier New", 50)
        self.font_small = pygame.font.SysFont("Courier New", 20)

        # Time of the last automatic movement.
        self.last_move_time = pygame.time.get_ticks()

    async def start(self):
        while self.running:

            # 1. Handle input. Keys change direction only.
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -20))

                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 20))

                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-20, 0))

                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((20, 0))

                    elif event.key == pygame.K_r and self.game_over:
                        self.snake.restart()
                        self.food.restart(self.snake.body)
                        self.score = 0
                        self.game_over = False
                        self.last_move_time = pygame.time.get_ticks()

            # 2. Move automatically, independently of keyboard input.
            now = pygame.time.get_ticks()

            if (
                self.running
                and not self.game_over
                and now - self.last_move_time >= MOVE_INTERVAL
            ):
                self.last_move_time = now

                # Determine the direction that Snake.move() will use.
                if self.snake.turn_queue:
                    direction = self.snake.turn_queue[0]
                else:
                    direction = self.snake.direction

                head_x, head_y = self.snake.body[0]
                dx, dy = direction

                next_head = (head_x + dx, head_y + dy)
                grow = next_head == self.food.position

                # Move the snake regardless of keyboard input.
                self.snake.move(grow=grow)

                # Check whether food was eaten.
                if self.snake.body[0] == self.food.position:
                    self.score += 1
                    self.food.position = self.food.relocate(
                        self.snake.body
                    )

                # Check wall collisions.
                head_x, head_y = self.snake.body[0]

                if (
                    head_x < 20
                    or head_x > 580
                    or head_y < 20
                    or head_y > 580
                ):
                    self.game_over = True

            # 3. Draw the current game state.
            self.screen.fill(BACKGROUND)

            self.snake.draw(self.screen)
            self.food.draw(self.screen)

            pygame.draw.rect(
                self.screen,
                (225, 225, 225),
                (0, 0, 600, 600),
                width=20,
            )

            pygame.draw.rect(
                self.screen,
                BACKGROUND,
                (0, 0, 600, 600),
                width=13,
            )

            score_surface = self.font.render(
                str(self.score), True, (255, 255, 255)
            )
            self.screen.blit(score_surface, (25, 25))

            if self.game_over:
                game_over_surface = self.font_game_over.render(
                    "GAME OVER", True, (50, 200, 80)
                )
                restart_surface = self.font_small.render(
                    "Press R to restart", True, (255, 255, 255)
                )

                self.screen.blit(game_over_surface, (170, 250))
                self.screen.blit(restart_surface, (20, 560))

            pygame.display.flip()

            # Let the browser process events and render frames.
            await asyncio.sleep(0)
