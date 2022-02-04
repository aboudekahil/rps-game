import math
import random, time, pygame, sys, threading
from perlin_noise import PerlinNoise

pygame.init()

SIZE_SCREEN = (WIDTH, HEIGHT) = (500, 500)          # SCREEN STUFF
GAME_SCREEN = pygame.display.set_mode(SIZE_SCREEN)  #

SCISSORS_TEXTURE = pygame.image.load("./0.png")
SCISSORS_TEXTURE = pygame.transform.scale(SCISSORS_TEXTURE, (30, 20))
PAPER_TEXTURE = pygame.image.load("./1.png")
PAPER_TEXTURE = pygame.transform.scale(PAPER_TEXTURE, (26, 28))
ROCK_TEXTURE = pygame.image.load("./2.png")
ROCK_TEXTURE = pygame.transform.scale(ROCK_TEXTURE, (25, 20))

entities = pygame.sprite.Group()

class Entity(pygame.sprite.Sprite):
    def __init__(self, type: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type = type

        match self.type:
            case 0:
                self.x = WIDTH // 2
                self.y = 36
                self.image = SCISSORS_TEXTURE
            case 1:
                self.x = 40
                self.y = 400
                self.image = PAPER_TEXTURE
            case 2:
                self.x = 460
                self.y = 400
                self.image = ROCK_TEXTURE
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.noise = PerlinNoise(octaves=random.randint(1, 9), seed=random.randint(0, 1000000))
    
    def setType(self, type):
        self.type = type
        match self.type:
            case 0:
                self.image = SCISSORS_TEXTURE
            case 1:
                self.image = PAPER_TEXTURE
            case 2:
                self.image = ROCK_TEXTURE

    def update(self) -> None:
        for entity in entities:
            if self != entity and self.rect.colliderect(entity.rect):
                if self.type == 0 and entity.type == 1:
                    entity.setType(0)
                elif self.type == 1 and entity.type == 2:
                    entity.setType(1)
                elif self.type == 2 and entity.type == 0:
                    entity.setType(2)

        
        self.x += random.randint(-2, 2)
        self.x = max(0, min(self.x, WIDTH - self.rect.width))

        self.y += random.randint(-2, 2)
        self.y = max(0, min(self.y, HEIGHT - self.rect.height))

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

def reset():
    for i in entities:
        entities.remove(i)
        del i
    for _ in range(10):
        entities.add(Entity(0))
        entities.add(Entity(1))
        entities.add(Entity(2))

def wait(seconds):
    time.sleep(seconds)
    reset()


def main() -> None:
    reset()
    running = True
    Clock = pygame.time.Clock()
    while running:
        Clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                # print("A")
                reset()

        GAME_SCREEN.fill((0, 0, 0))
        entities.update()
        entities.draw(GAME_SCREEN)
        if all(entity.type == 0 for entity in entities) or all(entity.type == 1 for entity in entities) or all(entity.type == 2 for entity in entities):
            SLEEP = threading.Thread(target=wait, args=[5])
            SLEEP.start()

        pygame.display.flip()


if __name__ == "__main__":
    main()
