# main.py
import pygame
import sys
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_RADIUS = 15
GRAVITY_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRAVITY_STRENGTH = 0.002  # Gravity strength
PLAYER_SPEED = 0.001  # Adjusted player speed
GOAL_RADIUS = 20  # Radius of the goal area

class Player:
    def __init__(self, x, y):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.sticking = False

    def update(self, obstacles):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.vy -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.vy += PLAYER_SPEED

        # Calculate the direction towards the gravity center
        if not self.sticking:
            dx = GRAVITY_CENTER[0] - self.x
            dy = GRAVITY_CENTER[1] - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.vx += dx * GRAVITY_STRENGTH
                self.vy += dy * GRAVITY_STRENGTH

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Check for collision with obstacles
        self.sticking = False
        player_rect = self.get_rect()
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                # Determine which side of the obstacle the player is on
                if self.vy > 0 and player_rect.bottom > obstacle.rect.top and keys[pygame.K_DOWN]:
                    self.y = obstacle.rect.top - PLAYER_RADIUS
                    self.vy = 0
                    self.sticking = True
                elif self.vy < 0 and player_rect.top < obstacle.rect.bottom and keys[pygame.K_UP]:
                    self.y = obstacle.rect.bottom + PLAYER_RADIUS
                    self.vy = 0
                    self.sticking = True
                if self.vx > 0 and player_rect.right > obstacle.rect.left and keys[pygame.K_RIGHT]:
                    self.x = obstacle.rect.left - PLAYER_RADIUS
                    self.vx = 0
                    self.sticking = True
                elif self.vx < 0 and player_rect.left < obstacle.rect.right and keys[pygame.K_LEFT]:
                    self.x = obstacle.rect.right + PLAYER_RADIUS
                    self.vx = 0
                    self.sticking = True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), PLAYER_RADIUS)

    def get_rect(self):
        return pygame.Rect(int(self.x) - PLAYER_RADIUS, int(self.y) - PLAYER_RADIUS, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.vx = 0
        self.vy = 0

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gravity Well")

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    obstacles = [
        Obstacle(300, 200, 50, 150),
        Obstacle(500, 400, 100, 50)
    ]

    # Define the goal area
    goal_position = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            print("Restarting level...")
            player.reset()

        screen.fill((0, 0, 0))

        player.update(obstacles)
        player.draw(screen)

        # Draw the goal area
        pygame.draw.circle(screen, (0, 255, 0), goal_position, GOAL_RADIUS)

        for obstacle in obstacles:
            obstacle.draw(screen)

        # Check if player reaches the goal
        if math.hypot(player.x - goal_position[0], player.y - goal_position[1]) <= GOAL_RADIUS + PLAYER_RADIUS:
            print("You Win!")
            running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()