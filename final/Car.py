import pygame
import sys
import os

# Init
pygame.init()

# Set working directory (adjust this to your asset folder path)
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
Entity_width = 300
Entity_height = 300
Entity_x = 500
Entity_y = 350
normal_speed = 5
run_speed = 9
speed = normal_speed

# Hitbox sizes (customize here)
# Idle hitbox (centered on character)
IDLE_HITBOX_WIDTH = 10
IDLE_HITBOX_HEIGHT = 10
IDLE_HITBOX_OFFSET_X = (Entity_width - IDLE_HITBOX_WIDTH) // 2
IDLE_HITBOX_OFFSET_Y = (Entity_height - IDLE_HITBOX_HEIGHT) // 2

# Attack hitbox (in front of character)
ATTACK_HITBOX_WIDTH = 30
ATTACK_HITBOX_HEIGHT = 30
ATTACK_HITBOX_OFFSET_Y = 10

# Movement limits
TOP_LIMIT_Y = HEIGHT - 290
BOTTOM_LIMIT_Y = HEIGHT - 100
LEFT_LIMIT_X = 0
RIGHT_LIMIT_X = WIDTH

# Load and scale images
def load_scaled(name):
    return pygame.transform.scale(pygame.image.load(name), (Entity_width, Entity_height))

entity_img1 = load_scaled("idleright_1.png")
entity_img2 = load_scaled("idleright_1.png")
entity_imgforward = load_scaled("idleright_1.png")
entity_imgbackward = load_scaled("idleright_1.png")

# Load idle right animation frames
idle_right_frames = [
    load_scaled(f"idleright_{i}.png") for i in range(1, 6)
]
idle_frame_index = 0
idle_last_update = pygame.time.get_ticks()
idle_frame_delay = 200

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
running_fast = False

# Attack state
attack1 = False
attack_duration = 300
attack_timer1 = 0

# Font and damage display
font = pygame.font.SysFont(None, 30)
damage_msg = ""
damage_timer = 0
damage_duration = 1000

# Health and Energy
max_health = 100
current_health = 100
max_energy = 100
current_energy = 100
energy_regen_rate = 0.2
run_energy_cost = 0.5

# Hitbox toggle
show_hitbox = False

# Draw bar utility
def draw_bar(surf, x, y, w, h, pct, color, border_color=(255, 255, 255)):
    pygame.draw.rect(surf, border_color, (x - 2, y - 2, w + 4, h + 4))
    fill = (pct / 100) * w
    pygame.draw.rect(surf, color, (x, y, fill, h))

# Function to get attack hitbox depending on facing
def get_attack_hitbox(x, y, width, height, facing):
    if facing == "right":
        return pygame.Rect(x + width, y + ATTACK_HITBOX_OFFSET_Y, ATTACK_HITBOX_WIDTH, ATTACK_HITBOX_HEIGHT)
    elif facing == "left":
        return pygame.Rect(x - ATTACK_HITBOX_WIDTH, y + ATTACK_HITBOX_OFFSET_Y, ATTACK_HITBOX_WIDTH, ATTACK_HITBOX_HEIGHT)
    elif facing == "up":
        return pygame.Rect(x + (width - ATTACK_HITBOX_WIDTH)//2, y - ATTACK_HITBOX_HEIGHT, ATTACK_HITBOX_WIDTH, ATTACK_HITBOX_HEIGHT)
    else:  # down
        return pygame.Rect(x + (width - ATTACK_HITBOX_WIDTH)//2, y + height, ATTACK_HITBOX_WIDTH, ATTACK_HITBOX_HEIGHT)

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
                facing1 = "left"
            if event.key == pygame.K_d:
                moving_right = True
                facing1 = "right"
            if event.key == pygame.K_w:
                moving_up = True
                facing1 = "up"
            if event.key == pygame.K_s:
                moving_down = True
                facing1 = "down"
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                running_fast = True
            if event.key == pygame.K_F1:
                show_hitbox = not show_hitbox

        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                running_fast = False

        # Left mouse attack
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            attack1 = True
            attack_timer1 = current_time

    # Speed and energy logic
    if running_fast and current_energy > 0:
        speed = run_speed
        current_energy -= run_energy_cost
        current_energy = max(0, current_energy)
    else:
        speed = normal_speed
        current_energy = min(current_energy + energy_regen_rate, max_energy)

    # Move entity
    if moving_right:
        Entity_x += speed
    if moving_left:
        Entity_x -= speed
    if moving_up:
        Entity_y -= speed
    if moving_down:
        Entity_y += speed

    # Clamp movement
    Entity_x = max(LEFT_LIMIT_X, min(Entity_x, RIGHT_LIMIT_X - Entity_width))
    Entity_y = max(TOP_LIMIT_Y - Entity_height, min(Entity_y, BOTTOM_LIMIT_Y - Entity_height))

    # Animate idle or movement
    if facing1 == "right" and not (moving_left or moving_right or moving_up or moving_down):
        if current_time - idle_last_update >= idle_frame_delay:
            idle_frame_index = (idle_frame_index + 1) % len(idle_right_frames)
            idle_last_update = current_time
        current_img1 = idle_right_frames[idle_frame_index]
    else:
        if current_time - last_switch_time >= frame_interval:
            current_img1 = entity_img2 if current_img1 == entity_img1 else entity_img1
            last_switch_time = current_time
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

    # Draw background and character
    DISPLAYSURF.blit(bg_image, (bg_x1, 0))
    DISPLAYSURF.blit(bg_image, (bg_x2, 0))
    DISPLAYSURF.blit(current_img1, (Entity_x, Entity_y))

    # Draw idle hitbox (centered)
    idle_hitbox_rect = pygame.Rect(
        int(Entity_x + IDLE_HITBOX_OFFSET_X),
        int(Entity_y + IDLE_HITBOX_OFFSET_Y),
        IDLE_HITBOX_WIDTH,
        IDLE_HITBOX_HEIGHT
    )
    if show_hitbox:
        pygame.draw.rect(DISPLAYSURF, (0, 255, 0), idle_hitbox_rect, 2)

    # Attack logic & draw attack hitbox
    if attack1 and current_time - attack_timer1 <=  attack_duration:
        attack_hitbox_rect = get_attack_hitbox(Entity_x, Entity_y, Entity_width, Entity_height, facing1)
        pygame.draw.rect(DISPLAYSURF, (255, 255, 0), attack_hitbox_rect, 2)
    else:
        attack1 = False

    # Damage message
    if damage_msg and current_time - damage_timer <= damage_duration:
        text = font.render(damage_msg, True, (255, 0, 0))
        DISPLAYSURF.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
    else:
        damage_msg = ""

    # Draw UI bars
    draw_bar(DISPLAYSURF, 20, HEIGHT - 60, 200, 20, current_health, (255, 0, 0))
    draw_bar(DISPLAYSURF, 20, HEIGHT - 30, 200, 20, current_energy, (0, 0, 255))
    DISPLAYSURF.blit(font.render(f'HP: {int(current_health)}', True, (255, 255, 255)), (230, HEIGHT - 60))
    DISPLAYSURF.blit(font.render(f'EN: {int(current_energy)}', True, (255, 255, 255)), (230, HEIGHT - 30))

    # Update display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
