import pygame
import sys
import random
import math

pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (135, 206, 235)      
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
FONT = pygame.font.SysFont("arial", 32)

gravity = 0.5
pipe_width = 60
pipe_gap = 175

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT // 2, 30, 30)
        self.movement = 0

    def update(self):
        self.movement += gravity
        self.rect.y += self.movement

    def flap(self):
        self.movement = -10

    def reset(self):
        self.rect.y = HEIGHT // 2
        self.movement = 0

class Pipe:
    def __init__(self, x):
        self.height = random.randint(100, 400)
        self.top = pygame.Rect(x, 0, pipe_width, self.height)
        self.bottom = pygame.Rect(x, self.height + pipe_gap, pipe_width, HEIGHT - self.height - pipe_gap)
        self.scored = False

    def move(self):
        self.top.x -= 4
        self.bottom.x -= 4

    def off_screen(self):
        return self.top.right < 0

def draw_mario_pipe(surface, pipe_rect, is_top=True):
    """Draw a pipe with Mario-style rectangular outline"""
    # Main pipe body
    pygame.draw.rect(surface, GREEN, pipe_rect)
    
    # Pipe outline (darker green)
    outline_color = (0, 100, 0)  # Darker green for outline
    outline_thickness = 3
    
    # Draw outline rectangles
    # Top outline
    top_outline = pygame.Rect(pipe_rect.x - outline_thickness, pipe_rect.y - outline_thickness, 
                             pipe_rect.width + outline_thickness * 2, outline_thickness)
    pygame.draw.rect(surface, outline_color, top_outline)
    
    # Bottom outline
    bottom_outline = pygame.Rect(pipe_rect.x - outline_thickness, pipe_rect.bottom, 
                                pipe_rect.width + outline_thickness * 2, outline_thickness)
    pygame.draw.rect(surface, outline_color, bottom_outline)
    
    # Left outline
    left_outline = pygame.Rect(pipe_rect.x - outline_thickness, pipe_rect.y - outline_thickness, 
                              outline_thickness, pipe_rect.height + outline_thickness * 2)
    pygame.draw.rect(surface, outline_color, left_outline)
    
    # Right outline
    right_outline = pygame.Rect(pipe_rect.right, pipe_rect.y - outline_thickness, 
                               outline_thickness, pipe_rect.height + outline_thickness * 2)
    pygame.draw.rect(surface, outline_color, right_outline)
    
    # Add pipe cap details for top pipe
    if is_top:
        # Bottom cap (wider rectangle at the bottom)
        cap_width = pipe_rect.width + 10
        cap_x = pipe_rect.x - 5
        cap_y = pipe_rect.bottom - 8
        cap_rect = pygame.Rect(cap_x, cap_y, cap_width, 8)
        pygame.draw.rect(surface, GREEN, cap_rect)
        
        # Cap outline
        cap_outline = pygame.Rect(cap_x - outline_thickness, cap_y - outline_thickness,
                                 cap_width + outline_thickness * 2, 8 + outline_thickness * 2)
        pygame.draw.rect(surface, outline_color, cap_outline)
    else:
        # Top cap (wider rectangle at the top) for bottom pipe
        cap_width = pipe_rect.width + 10
        cap_x = pipe_rect.x - 5
        cap_y = pipe_rect.y
        cap_rect = pygame.Rect(cap_x, cap_y, cap_width, 8)
        pygame.draw.rect(surface, GREEN, cap_rect)
        
        # Cap outline
        cap_outline = pygame.Rect(cap_x - outline_thickness, cap_y - outline_thickness,
                                 cap_width + outline_thickness * 2, 8 + outline_thickness * 2)
        pygame.draw.rect(surface, outline_color, cap_outline)

def draw_cartoon_bird(surface, bird_rect, bird_movement):
    """Draw a cartoon bird with body, head, beak, eyes, and wings"""
    x, y = bird_rect.x, bird_rect.y
    width, height = bird_rect.width, bird_rect.height
    
    # Bird body (main circle)
    body_radius = min(width, height) // 2
    body_center = (x + width // 2, y + height // 2)
    
    # Wings (animated based on movement)
    wing_angle = math.sin(pygame.time.get_ticks() * 0.01) * 0.3
    if bird_movement < 0:  # Flapping up
        wing_angle = -0.5
    
    # Right wing (drawn behind the body)
    wing_points_right = [
        (body_center[0] + body_radius // 2, body_center[1] - body_radius // 3),
        (body_center[0] + body_radius, body_center[1] - body_radius // 2 + int(wing_angle * 10)),
        (body_center[0] + body_radius // 2, body_center[1] + body_radius // 3)
    ]
    pygame.draw.polygon(surface, ORANGE, wing_points_right)
    
    # Bird body (main circle) - drawn after right wing
    pygame.draw.circle(surface, YELLOW, body_center, body_radius)
    
    # Bird head (smaller circle)
    head_radius = body_radius // 2
    head_center = (body_center[0] + body_radius // 2, body_center[1] - body_radius // 3)
    pygame.draw.circle(surface, YELLOW, head_center, head_radius)
    
    # Eyes
    eye_radius = 3
    left_eye = (head_center[0] - 3, head_center[1] - 2)
    right_eye = (head_center[0] + 3, head_center[1] - 2)
    pygame.draw.circle(surface, BLACK, left_eye, eye_radius)
    pygame.draw.circle(surface, BLACK, right_eye, eye_radius)
    
    # Eye highlights
    pygame.draw.circle(surface, WHITE, (left_eye[0] - 1, left_eye[1] - 1), 1)
    pygame.draw.circle(surface, WHITE, (right_eye[0] - 1, right_eye[1] - 1), 1)
    
    # Beak (small triangle pointing towards bird)
    beak_points = [
        (head_center[0] + head_radius - 2, head_center[1] + 2),
        (head_center[0] + head_radius - 8, head_center[1]),
        (head_center[0] + head_radius - 8, head_center[1] + 4)
    ]
    pygame.draw.polygon(surface, ORANGE, beak_points)
    
    # Left wing (drawn after body)
    wing_points_left = [
        (body_center[0] - body_radius // 2, body_center[1] - body_radius // 3),
        (body_center[0] - body_radius, body_center[1] - body_radius // 2 + int(wing_angle * 10)),
        (body_center[0] - body_radius // 2, body_center[1] + body_radius // 3)
    ]
    pygame.draw.polygon(surface, ORANGE, wing_points_left)

def main():
    bird = Bird()
    pipes = []
    score = 0
    high_score = 0
    game_active = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.flap()
                    else:
                        bird.reset()
                        pipes.clear()
                        score = 0
                        game_active = True
            if event.type == SPAWNPIPE and game_active:
                pipes.append(Pipe(WIDTH))

        if game_active:
            bird.update()
            for pipe in pipes:
                pipe.move()
            pipes = [pipe for pipe in pipes if not pipe.off_screen()]

            # Collision
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                    game_active = False
            if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
                game_active = False

            # Scoring
            for pipe in pipes:
                if pipe.top.right < bird.rect.left and not pipe.scored:
                    score += 1
                    pipe.scored = True

        WIN.fill(BLUE)
        if game_active:
            draw_cartoon_bird(WIN, bird.rect, bird.movement)
            for pipe in pipes:
                draw_mario_pipe(WIN, pipe.top, is_top=True)
                draw_mario_pipe(WIN, pipe.bottom, is_top=False)
            score_text = FONT.render(f"Score: {score}", True, BLACK)
            WIN.blit(score_text, (10, 10))
        else:
            game_over_text = FONT.render("GAME OVER", True, BLACK)
            WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
            restart_text = FONT.render("PRESS SPACE TO RESTART", True, BLACK)
            WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
            if score > high_score:
                high_score = score
            hs_text = FONT.render(f"High Score: {high_score}", True, BLACK)
            WIN.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()


