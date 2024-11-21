import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sushi Snow Battle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SNOW_COLOR = (200, 200, 250)


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, is_bot=False):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.health = 100
        self.is_bot = is_bot
        self.snowball_cooldown = 0

    def move(self):
        if not self.is_bot:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
        else:
            # Simple AI movement
            self.rect.x += random.randint(-1, 1) * self.speed
            self.rect.y += random.randint(-1, 1) * self.speed

        # Keep player on screen
        self.rect.clamp_ip(screen.get_rect())

        if self.snowball_cooldown > 0:
            self.snowball_cooldown -= 1

    def throw_snowball(self, target_x, target_y):
        if self.snowball_cooldown == 0:
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance == 0:
                return None
            speed = 10
            vx = dx / distance * speed
            vy = dy / distance * speed
            snowball = Snowball(self.rect.centerx, self.rect.centery, vx, vy)
            self.snowball_cooldown = (
                30  # Set cooldown to 30 frames (0.5 seconds at 60 FPS)
            )
            return snowball
        return None


# Snowball class
class Snowball(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, SNOW_COLOR, (5, 5), 5)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Remove snowball if it goes off-screen
        if not screen.get_rect().colliderect(self.rect):
            self.kill()


# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect(center=(x, y))


# Create sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
snowballs = pygame.sprite.Group()

# Create player
sushi = Player(WIDTH // 2, HEIGHT // 2, BLUE)
players.add(sushi)
all_sprites.add(sushi)

# Create bots
for _ in range(5):
    bot = Player(random.randint(0, WIDTH), random.randint(0, HEIGHT), RED, is_bot=True)
    players.add(bot)
    all_sprites.add(bot)

# Create obstacles
for _ in range(10):
    obstacle = Obstacle(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Player throws snowball on left mouse click
            snowball = sushi.throw_snowball(*event.pos)
            if snowball:
                snowballs.add(snowball)
                all_sprites.add(snowball)

    # Update
    for player in players:
        player.move()
        if (
            player.is_bot and random.random() < 0.02
        ):  # 2% chance each frame for bot to throw snowball
            target = random.choice(list(players))
            snowball = player.throw_snowball(target.rect.centerx, target.rect.centery)
            if snowball:
                snowballs.add(snowball)
                all_sprites.add(snowball)

    snowballs.update()

    # Check for collisions
    for player in players:
        if pygame.sprite.spritecollide(player, obstacles, False):
            player.health -= 0.5

        hit_snowballs = pygame.sprite.spritecollide(player, snowballs, True)
        for _ in hit_snowballs:
            player.health -= 10

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Draw health bars
    for player in players:
        pygame.draw.rect(
            screen, RED, (player.rect.x, player.rect.y - 10, player.rect.width, 5)
        )
        pygame.draw.rect(
            screen,
            GREEN,
            (
                player.rect.x,
                player.rect.y - 10,
                player.rect.width * (player.health / 100),
                5,
            ),
        )

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
