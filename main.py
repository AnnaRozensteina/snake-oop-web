
import asyncio
import pygame
import traceback
import textwrap
from game import Game

async def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    font = pygame.font.SysFont("Courier New", 18)

    try:
        screen.fill((25, 25, 25))
        screen.blit(font.render("Creating Game...", True, (255, 255, 255)), (20, 20))
        pygame.display.flip()

        game = Game()

        screen.fill((25, 25, 25))
        screen.blit(font.render("Starting game loop...", True, (255, 255, 255)), (20, 20))
        pygame.display.flip()

        await game.start()

    except Exception:
        error_lines = traceback.format_exc().splitlines()
        lines = []
        for line in error_lines:
            lines.extend(textwrap.wrap(line, width=55) or [""])

        screen = pygame.display.get_surface()
        screen.fill((25, 25, 25))

        for i, line in enumerate(lines[-25:]):
            screen.blit(
                font.render(line[:65], True, (255, 100, 100)),
                (10, 10 + i * 22)
            )

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            await asyncio.sleep(0)

asyncio.run(main())
