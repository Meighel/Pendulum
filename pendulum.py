import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Pendulum properties
origin = (WIDTH // 2, 100)
length = 250
radius = 20
mass = 1
gravity = 9.8
friction = 0.001
angle = math.pi / 4
omega = 0

# Time properties
FPS = 60
dt = 1 / FPS
clock = pygame.time.Clock()

# Dragging state
is_dragging = False
dragging_gravity = dragging_friction = dragging_length = dragging_mass = False

# Slider properties
slider_gravity = pygame.Rect(50, HEIGHT - 190, 300, 10)
slider_friction = pygame.Rect(50, HEIGHT - 130, 300, 10)
slider_length = pygame.Rect(50, HEIGHT - 70, 300, 10)
slider_mass = pygame.Rect(50, HEIGHT - 20, 300, 10)

handle_gravity = pygame.Rect(50 + int(gravity / 50 * 300), HEIGHT - 195, 10, 20)
handle_friction = pygame.Rect(50 + int(friction * 100 * 300), HEIGHT - 135, 10, 20)
handle_length = pygame.Rect(50 + int(length / 400 * 300), HEIGHT - 75, 10, 20)
handle_mass = pygame.Rect(50 + int(mass / 10 * 300), HEIGHT - 25, 10, 20)


def calculate_alpha():
    """Calculate the angular acceleration."""
    return (-gravity / (length / 100)) * math.sin(angle) - friction * omega


def get_pendulum_position(angle):
    """Calculate the (x, y) position of the pendulum bob."""
    x = origin[0] + length * math.sin(angle)
    y = origin[1] + length * math.cos(angle)
    return int(x), int(y)


def draw_sliders():
    """Draw sliders for gravity, friction, length, and mass adjustment."""
    pygame.draw.rect(screen, GRAY, slider_gravity)
    pygame.draw.rect(screen, BLACK, handle_gravity)
    pygame.draw.rect(screen, GRAY, slider_friction)
    pygame.draw.rect(screen, BLACK, handle_friction)
    pygame.draw.rect(screen, GRAY, slider_length)
    pygame.draw.rect(screen, BLACK, handle_length)
    pygame.draw.rect(screen, GRAY, slider_mass)
    pygame.draw.rect(screen, BLACK, handle_mass)

    font = pygame.font.SysFont(None, 24)
    gravity_label = font.render(f"Gravity: {gravity:.2f}", True, BLACK)
    friction_label = font.render(f"Friction: {friction:.4f}", True, BLACK)
    length_label = font.render(f"Length: {length:.2f}", True, BLACK)
    mass_label = font.render(f"Mass: {mass:.2f}", True, BLACK)

    screen.blit(gravity_label, (50, HEIGHT - 220))
    screen.blit(friction_label, (50, HEIGHT - 160))
    screen.blit(length_label, (50, HEIGHT - 100))
    screen.blit(mass_label, (50, HEIGHT - 50))


def draw_energy_bar():
    """Draw the energy meter showing KE and PE energy."""
    max_height = 200
    bar_width = 40
    bar_x = WIDTH - 150
    bar_y = HEIGHT - 220

    # Energy calculations
    ke = 0.5 * mass * (length * omega) ** 2
    pe = mass * gravity * (origin[1] + length - get_pendulum_position(angle)[1])
    total_energy = ke + pe

    # Scale factors
    energy_scale = max_height / max(total_energy, 1)

    # Draw energy bars
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, max_height))  # Background
    pygame.draw.rect(screen, RED, (bar_x, bar_y + max_height - int(pe * energy_scale), bar_width, int(pe * energy_scale)))  # PE
    pygame.draw.rect(screen, BLUE, (bar_x + bar_width, bar_y + max_height - int(ke * energy_scale), bar_width, int(ke * energy_scale)))  # KE

    # Labels
    font = pygame.font.SysFont(None, 24)
    pe_label = font.render("PE", True, BLACK)
    ke_label = font.render("KE", True, BLACK)

    screen.blit(pe_label, (bar_x, bar_y + max_height + 5))
    screen.blit(ke_label, (bar_x + bar_width, bar_y + max_height + 5))


# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bob_x, bob_y = get_pendulum_position(angle)
            distance = math.sqrt((mouse_x - bob_x) ** 2 + (mouse_y - bob_y) ** 2)
            if distance <= radius:
                is_dragging = True

            if handle_gravity.collidepoint(mouse_x, mouse_y):
                dragging_gravity = True
            if handle_friction.collidepoint(mouse_x, mouse_y):
                dragging_friction = True
            if handle_length.collidepoint(mouse_x, mouse_y):
                dragging_length = True
            if handle_mass.collidepoint(mouse_x, mouse_y):
                dragging_mass = True

        if event.type == pygame.MOUSEBUTTONUP:
            is_dragging = dragging_gravity = dragging_friction = dragging_length = dragging_mass = False

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if dragging_gravity:
            handle_gravity.x = max(slider_gravity.x, min(mouse_x, slider_gravity.x + slider_gravity.width))
            gravity = ((handle_gravity.x - slider_gravity.x) / slider_gravity.width) * 50
        if dragging_friction:
            handle_friction.x = max(slider_friction.x, min(mouse_x, slider_friction.x + slider_friction.width))
            friction = ((handle_friction.x - slider_friction.x) / slider_friction.width) / 100
        if dragging_length:
            handle_length.x = max(slider_length.x, min(mouse_x, slider_length.x + slider_length.width))
            length = ((handle_length.x - slider_length.x) / slider_length.width) * 400
        if dragging_mass:
            handle_mass.x = max(slider_mass.x, min(mouse_x, slider_mass.x + slider_mass.width))
            mass = ((handle_mass.x - slider_mass.x) / slider_mass.width) * 10

    if is_dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - origin[0]
        dy = mouse_y - origin[1]
        angle = math.atan2(dx, dy)
        omega = 0
    else:
        alpha = calculate_alpha()
        omega += alpha * dt
        angle += omega * dt
        omega *= (1 - friction)

    # Draw the y-line (vertical reference line)
    pygame.draw.line(screen, BLACK, origin, (origin[0], HEIGHT), 1)

    # Draw the x-line (horizontal reference line at the top of the y-line)
    pygame.draw.line(screen, BLACK, (0, origin[1]), (WIDTH, origin[1]), 1)

    pygame.draw.line(screen, BLACK, origin, get_pendulum_position(angle), 2)
    pygame.draw.circle(screen, RED, get_pendulum_position(angle), radius)

    draw_sliders()
    draw_energy_bar()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
