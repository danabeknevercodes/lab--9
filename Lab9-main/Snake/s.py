import pygame
import random
import time

pygame.init()

BLOCK_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = BLOCK_SIZE * GRID_WIDTH
HEIGHT = BLOCK_SIZE * GRID_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Borders")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

font = pygame.font.SysFont("Verdana", 20)

clock = pygame.time.Clock()
speed = 5

snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_dir = (1, 0)

class Food:
    def __init__(self):
        self.generate()
    
    def generate(self):
        self.position = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
        self.value = random.choice([1, 2, 3])
        self.spawn_time = time.time()
    
    def is_expired(self, duration=5):
        return time.time() - self.spawn_time > duration

food = Food()

score = 0
level = 1
running = True

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, 1):
                snake_dir = (0, -1)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -1):
                snake_dir = (0, 1)
            elif event.key == pygame.K_LEFT and snake_dir != (1, 0):
                snake_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                snake_dir = (1, 0)

    head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    if head[0] == 0 or head[0] == GRID_WIDTH - 1 or head[1] == 0 or head[1] == GRID_HEIGHT - 1:
        print("Вы проиграли: столкновение с границей")
        break

    if head in snake:
        print("Вы проиграли: столкновение с собой")
        break

    snake.insert(0, head)

    if head == food.position:
        score += food.value
        food.generate()

        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    if food.is_expired():
        food.generate()

    screen.fill(BLACK)

    for x in range(GRID_WIDTH):
        pygame.draw.rect(screen, BLUE, (x * BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BLUE, (x * BLOCK_SIZE, (GRID_HEIGHT - 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for y in range(GRID_HEIGHT):
        pygame.draw.rect(screen, BLUE, (0, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BLUE, ((GRID_WIDTH - 1) * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(screen, RED, (food.position[0] * BLOCK_SIZE, food.position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()