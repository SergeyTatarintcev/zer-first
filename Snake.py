import pygame
import random
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
CONTROL_PANEL_HEIGHT = 100
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (50, 50, 50)
FRAME_COLOR = BLUE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Кнопки управления
BUTTONS = {
    "UP": pygame.Rect(370, HEIGHT - 80, 60, 30),
    "DOWN": pygame.Rect(370, HEIGHT - 40, 60, 30),
    "LEFT": pygame.Rect(310, HEIGHT - 40, 60, 30),
    "RIGHT": pygame.Rect(430, HEIGHT - 40, 60, 30),
}

def draw_buttons():
    for direction, rect in BUTTONS.items():
        pygame.draw.rect(screen, GRAY, rect, border_radius=5)
        text = font.render(direction, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_frame():
    pygame.draw.rect(screen, FRAME_COLOR, (0, 0, WIDTH, HEIGHT - CONTROL_PANEL_HEIGHT), 4)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, RED, (*position, CELL_SIZE, CELL_SIZE))

def get_random_position():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CONTROL_PANEL_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return (x, y)

def main():
    snake = [(100, 100)]
    direction = RIGHT
    food = get_random_position()
    score = 0
    speed = 5  # Начальная скорость снижена

    running = True
    while running:
        screen.fill(BLACK)

        draw_snake(snake)
        draw_food(food)
        draw_frame()
        draw_buttons()

        # Очки
        score_text = font.render(f"Очки: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for dir_name, rect in BUTTONS.items():
                    if rect.collidepoint(mx, my):
                        if dir_name == "UP" and direction != DOWN:
                            direction = UP
                        elif dir_name == "DOWN" and direction != UP:
                            direction = DOWN
                        elif dir_name == "LEFT" and direction != RIGHT:
                            direction = LEFT
                        elif dir_name == "RIGHT" and direction != LEFT:
                            direction = RIGHT

        # Обновление позиции змейки
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx * CELL_SIZE, head_y + dy * CELL_SIZE)

        # Столкновения
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT - CONTROL_PANEL_HEIGHT or
            new_head in snake
        ):
            print("Игра окончена")
            running = False

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = get_random_position()
            if score % 5 == 0:
                speed += 1  # Увеличение скорости
        else:
            snake.pop()

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
