import pygame
import sys
import os

# Init
pygame.init()

# Set working directory (where castle.png etc. are stored)
os.chdir("D:/GithubPython/final")

# Window setup
WIDTH = 1014
HEIGHT = 594
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Background")

# Load and prepare background
bg_image = pygame.image.load('castle.png').convert()
bg_width = bg_image.get_width()

# Character setup
Entity_width = 50
Entity_height = 100
Entity_x = 500
Entity_y = 350
speed = 5

# Movement limits
TOP_LIMIT_Y = HEIGHT - 290
BOTTOM_LIMIT_Y = HEIGHT - 100
LEFT_LIMIT_X = 0
RIGHT_LIMIT_X = WIDTH

# Load and scale images
entity_img1 = pygame.image.load("gamble.png")
entity_img2 = pygame.image.load("gamble2.png")
entity_imgforward = pygame.image.load("run.png")
entity_imgbackward = pygame.image.load("gamblebackwards.png")

entity_img1 = pygame.transform.scale(entity_img1, (Entity_width, Entity_height))
entity_img2 = pygame.transform.scale(entity_img2, (Entity_width, Entity_height))
entity_imgforward = pygame.transform.scale(entity_imgforward, (Entity_width, Entity_height))
entity_imgbackward = pygame.transform.scale(entity_imgbackward, (Entity_width, Entity_height))

# Animation state
current_img1 = entity_img1
last_switch_time = pygame.time.get_ticks()
frame_interval = 100

# Background scroll
bg_x1 = 0
bg_x2 = bg_width
scroll_speed = 10

# Movement and direction
moving_right = moving_left = moving_up = moving_down = False
facing1 = "right"

# Attack state
attack1 = False
attack_duration = 300  # ms
attack_timer1 = 0

# Font and damage display
font = pygame.font.SysFont(None, 30)
damage_msg = ""
damage_timer = 0
damage_duration = 1000  # 1 second

clock = pygame.time.Clock()
running = True

# MAIN LOOP
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
                facing1 = "left"
            if event.key == pygame.K_RIGHT:
                moving_right = True
                facing1 = "right"
            if event.key == pygame.K_UP:
                moving_up = True
                facing1 = "up"
            if event.key == pygame.K_DOWN:
                moving_down = True
                facing1 = "down"
            if event.key == pygame.K_SLASH:
                attack1 = True
                attack_timer1 = current_time

        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_DOWN:
                moving_down = False

    # Move player
    if moving_right:
        Entity_x += speed
    if moving_left:
        Entity_x -= speed
    if moving_up:
        Entity_y -= speed
    if moving_down:
        Entity_y += speed

    # Clamp player position
    Entity_x = max(LEFT_LIMIT_X, min(Entity_x, RIGHT_LIMIT_X - Entity_width))
    Entity_y = max(TOP_LIMIT_Y - Entity_height, min(Entity_y, BOTTOM_LIMIT_Y - Entity_height))

    # Animate (idle toggle)
    if current_time - last_switch_time >= frame_interval:
        current_img1 = entity_img2 if current_img1 == entity_img1 else entity_img1
        last_switch_time = current_time

    # Set correct image for direction
    if moving_right:
        current_img1 = entity_imgforward
    elif moving_left:
        current_img1 = entity_imgbackward

    # Scroll background
    if moving_right and Entity_x > WIDTH // 2:
        bg_x1 -= scroll_speed
        bg_x2 -= scroll_speed
    elif moving_left and Entity_x < WIDTH // 2:
        bg_x1 += scroll_speed
        bg_x2 += scroll_speed

    # Loop background
    if bg_x1 <= -bg_width:
        bg_x1 = bg_x2 + bg_width
    if bg_x2 <= -bg_width:
        bg_x2 = bg_x1 + bg_width
    if bg_x1 >= bg_width:
        bg_x1 = bg_x2 - bg_width
    if bg_x2 >= bg_width:
        bg_x2 = bg_x1 - bg_width

    # Draw everything
    DISPLAYSURF.blit(bg_image, (bg_x1, 0))
    DISPLAYSURF.blit(bg_image, (bg_x2, 0))

    # Player rect
    rect1 = pygame.Rect(Entity_x, Entity_y, Entity_width, Entity_height)
    DISPLAYSURF.blit(current_img1, (Entity_x, Entity_y))

    # Draw borders
    pygame.draw.line(DISPLAYSURF, (255, 0, 0), (0, TOP_LIMIT_Y), (WIDTH, TOP_LIMIT_Y), 2)
    pygame.draw.line(DISPLAYSURF, (255, 0, 0), (0, BOTTOM_LIMIT_Y), (WIDTH, BOTTOM_LIMIT_Y), 2)
    pygame.draw.line(DISPLAYSURF, (255, 0, 0), (LEFT_LIMIT_X, 0), (LEFT_LIMIT_X, HEIGHT), 2)
    pygame.draw.line(DISPLAYSURF, (255, 0, 0), (RIGHT_LIMIT_X, 0), (RIGHT_LIMIT_X, HEIGHT), 2)

    # Attack hitbox function
    def get_hitbox(x, y, width, height, facing):
        hitbox_width = 30
        hitbox_height = 30
        if facing == "right":
            return pygame.Rect(x + width, y + height//2 - hitbox_height//2, hitbox_width, hitbox_height)
        elif facing == "left":
            return pygame.Rect(x - hitbox_width, y + height//2 - hitbox_height//2, hitbox_width, hitbox_height)
        elif facing == "up":
            return pygame.Rect(x + width//2 - hitbox_width//2, y - hitbox_height, hitbox_width, hitbox_height)
        else:  # down
            return pygame.Rect(x + width//2 - hitbox_width//2, y + height, hitbox_width, hitbox_height)

    # Player attack
    if attack1 and current_time - attack_timer1 <= attack_duration:
        hitbox1 = get_hitbox(Entity_x, Entity_y, Entity_width, Entity_height, facing1)
        pygame.draw.rect(DISPLAYSURF, (255, 255, 0), hitbox1, 2)  # Show yellow hitbox
    else:
        attack1 = False

    # Display damage message
    if damage_msg and current_time - damage_timer <= damage_duration:
        text = font.render(damage_msg, True, (255, 0, 0))
        DISPLAYSURF.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
    else:
        damage_msg = ""

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
