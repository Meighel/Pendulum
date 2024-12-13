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

# Pendulum properties
origin = (WIDTH // 2, 100)  # Pivot point
length = 250               # Length of pendulum string (in pixels, proportional to meters)
radius = 20                # Radius of pendulum bob
mass = 1                   # Mass of pendulum bob (in kg)
gravity = 9.8              # Initial gravity constant (m/s^2)
friction = 0.001            # Initial air friction
angle = math.pi / 4        # Initial angle (45 degrees)
omega = 0                  # Angular velocity
alpha = 0                  # Angular acceleration

# Time properties
FPS = 60
dt = 1 / FPS  # Time step in seconds
clock = pygame.time.Clock()

# Dragging state
is_dragging = False
dragging_gravity = False
dragging_friction = False
dragging_length = False
dragging_mass = False

# Slider properties
slider_gravity = pygame.Rect(50, HEIGHT - 190, 300, 10)  # Widen the gravity slider
slider_friction = pygame.Rect(50, HEIGHT - 130, 300, 10)  # Widen the friction slider
slider_length = pygame.Rect(50, HEIGHT - 70, 300, 10)  # Widen the length slider
slider_mass = pygame.Rect(50, HEIGHT - 20, 300, 10)  # Widen the mass slider

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

    # Labels and values
    gravity_label = font.render(f"Gravity: {gravity:.2f}", True, BLACK)
    friction_label = font.render(f"Friction: {friction:.4f}", True, BLACK)
    length_label = font.render(f"Length: {length:.2f}", True, BLACK)
    mass_label = font.render(f"Mass: {mass:.2f}", True, BLACK)

    screen.blit(gravity_label, (50, HEIGHT - 220))
    screen.blit(friction_label, (50, HEIGHT - 160))
    screen.blit(length_label, (50, HEIGHT - 100))
    screen.blit(mass_label, (50, HEIGHT - 50))


# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the pendulum bob is clicked
            bob_x, bob_y = get_pendulum_position(angle)
            distance = math.sqrt((mouse_x - bob_x)**2 + (mouse_y - bob_y)**2)
            if distance <= radius:
                is_dragging = True

            # Check if gravity slider handle is clicked
            if handle_gravity.collidepoint(mouse_x, mouse_y):
                dragging_gravity = True

            # Check if friction slider handle is clicked
            if handle_friction.collidepoint(mouse_x, mouse_y):
                dragging_friction = True

            # Check if length slider handle is clicked
            if handle_length.collidepoint(mouse_x, mouse_y):
                dragging_length = True

            # Check if mass slider handle is clicked
            if handle_mass.collidepoint(mouse_x, mouse_y):
                dragging_mass = True

        # Stop dragging
        if event.type == pygame.MOUSEBUTTONUP:
            is_dragging = False
            dragging_gravity = False
            dragging_friction = False
            dragging_length = False
            dragging_mass = False

    # Dragging logic for pendulum
    if is_dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - origin[0]
        dy = mouse_y - origin[1]
        angle = math.atan2(dx, dy)
        omega = 0  # Reset velocity when dragging

    # Dragging logic for sliders
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Gravity slider
        if dragging_gravity:
            handle_gravity.x = max(slider_gravity.x, min(mouse_x, slider_gravity.x + slider_gravity.width))
            gravity = ((handle_gravity.x - slider_gravity.x) / slider_gravity.width) * 50  # Gravity range expanded to 50

        # Friction slider
        if dragging_friction:
            handle_friction.x = max(slider_friction.x, min(mouse_x, slider_friction.x + slider_friction.width))
            friction = ((handle_friction.x - slider_friction.x) / slider_friction.width) / 100  # Friction range expanded

        # Length slider
        if dragging_length:
            handle_length.x = max(slider_length.x, min(mouse_x, slider_length.x + slider_length.width))
            length = ((handle_length.x - slider_length.x) / slider_length.width) * 400  # Length range expanded

        # Mass slider
        if dragging_mass:
            handle_mass.x = max(slider_mass.x, min(mouse_x, slider_mass.x + slider_mass.width))
            mass = ((handle_mass.x - slider_mass.x) / slider_mass.width) * 10  # Mass range expanded

    # Pendulum physics
    if not is_dragging:
        alpha = calculate_alpha()
        omega += alpha * dt
        angle += omega * dt
        omega *= (1 - friction)  # Apply friction damping

    # Draw y-axis
    pygame.draw.line(screen, BLUE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    # Draw pendulum
    bob_x, bob_y = get_pendulum_position(angle)
    pygame.draw.line(screen, BLACK, origin, (bob_x, bob_y), 2)
    pygame.draw.circle(screen, RED, (bob_x, bob_y), radius)

    # Draw sliders
    draw_sliders()

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
