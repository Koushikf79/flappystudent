import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 400
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Game settings
gravity = 0.5
flap_power = -10
pipe_speed = 5
pipe_gap = 150

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load("assets/bird.png")
background_img = pygame.image.load("assets/background.png")
pipe_img = pygame.image.load("assets/pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (pipe_img.get_width(), screen_height))

# Fonts
font = pygame.font.SysFont("comicsansms", 35)

# High score file
high_score_file = "high_score.txt"

# Function to load high score
def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read())
    return 0

# Function to save high score
def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Load high score
high_score = load_high_score()

class Bird:
    def __init__(self, x, y):
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0

    def update(self):
        self.velocity += gravity
        self.rect.y += int(self.velocity)

    def flap(self):
        self.velocity = flap_power

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self, x, height, gap):
        self.image = pipe_img
        self.rect_top = self.image.get_rect()
        self.rect_bottom = self.image.get_rect()
        self.rect_top.bottomleft = (x, height)
        self.rect_bottom.topleft = (x, height + gap)
        self.passed = False

    def update(self):
        self.rect_top.x -= pipe_speed
        self.rect_bottom.x -= pipe_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect_top, (0, screen_height - self.rect_top.height, self.rect_top.width, self.rect_top.height))
        screen.blit(self.image, self.rect_bottom, (0, 0, self.rect_bottom.width, self.rect_bottom.height))

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(screen, text, font, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x - width // 2, y - height // 2, width, height))
    draw_text(screen, text, font, white, x, y)

def game_loop():
    global high_score
    bird = Bird(screen_width // 4, screen_height // 2)
    pipes = []
    score = 0
    clock = pygame.time.Clock()
    running = True
    game_over = False

    def reset_game():
        nonlocal bird, pipes, score, game_over
        bird = Bird(screen_width // 4, screen_height // 2)
        pipes = []
        score = 0
        game_over = False

    while running:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_over and restart_button.collidepoint((mouse_x, mouse_y)):
                    reset_game()

        if not game_over:
            bird.update()

            if len(pipes) == 0 or pipes[-1].rect_top.right < screen_width - 200:
                pipe_height = random.randint(100, screen_height - 200)
                pipes.append(Pipe(screen_width, pipe_height, pipe_gap))

            for pipe in pipes:
                pipe.update()
                if pipe.rect_top.right < 0:
                    pipes.remove(pipe)
                if not pipe.passed and pipe.rect_top.right < bird.rect.left:
                    pipe.passed = True
                    score += 1

            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect_top) or bird.rect.colliderect(pipe.rect_bottom):
                    game_over = True

            if bird.rect.top < 0 or bird.rect.bottom > screen_height:
                game_over = True

            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)

        if game_over:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            
            draw_text(screen, "Game Over", font, red, screen_width // 2, screen_height // 3)
            restart_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2, 100, 50)
            draw_button(screen, "Restart", font, green, screen_width // 2, screen_height // 2, 100, 50)

        score_text = font.render("Score: " + str(score), True, black)
        high_score_text = font.render("High Score: " + str(high_score), True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
