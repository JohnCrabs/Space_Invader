import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_MARGIN = 5
COLLISION = 100


def isCollision(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    dist = dx*dx + dy*dy
    if dist <= COLLISION:
        return True
    return False


class Character:
    def __init__(self):
        self.name = "player"
        self.sprite = None
        self.sprite_w = 0
        self.sprite_h = 0
        self.coord_X = 0
        self.coord_Y = 0
        self.speed_X = 0.5
        self.speed_Y = 0.5

    def set(self, name, sprite, sprite_width, sprite_height, x, y, speed_X=0.5, speed_Y=0.5):
        self.name = name
        self.sprite = sprite
        self.sprite_w = sprite_width
        self.sprite_h = sprite_height
        self.coord_X = x
        self.coord_Y = y
        self.speed_X = speed_X
        self.speed_Y = speed_Y

    def set_random_coordinated(self, x_min, x_max, y_min, y_max):
        self.coord_X = random.randint(x_min, x_max)
        self.coord_Y = random.randint(y_min, y_max)

    def move(self, dx=0.0, dy=0.0):
        self.coord_X += dx
        self.coord_Y += dy

    def draw(self, screen):
        screen.blit(self.sprite, (self.coord_X, self.coord_Y))


class SpaceInvaders:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set title
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("sprites/spaceship.png")
        pygame.display.set_icon(icon)

        # Set score
        self.score_value = 0

        # Set Clock
        self.clock = pygame.time.Clock()

        # Set player
        sprite = pygame.image.load("sprites/playership.png")
        p_w, p_h = sprite.get_rect().size
        self.player = Character()
        self.player.set("spaceship", sprite, p_w, p_h, SCREEN_WIDTH / 2 - p_w / 2,
                        SCREEN_HEIGHT - p_h - p_h / 2, speed_X=6)

        # Set bullet
        # sprite = pygame.image.load("sprites/rocket.png")
        sprite = pygame.image.load("sprites/rocket_16_x_16.png")
        p_w, p_h = sprite.get_rect().size
        self.rocket = Character()
        self.rocket.set("rocket", sprite, p_w, p_h, SCREEN_WIDTH / 2 - p_w / 2,
                        SCREEN_HEIGHT - p_h - p_h / 2, speed_Y=-10)

        # Set enemy
        self.enemy = []
        self.enemy_fleet = 1
        for i in range(self.enemy_fleet):
            self.enemy.append(self.create_enemy())

        # Set background
        self.background = pygame.image.load("sprites/universe.png")

    def set_text_info(self):
        font = pygame.font.Font("freesansbold.ttf", 16)
        score = font.render("Score : " + str(self.score_value), True, (200, 0, 0))
        enemy_fleet = font.render("Enemy Fleet : " + str(self.enemy_fleet),  True, (200, 0, 0))
        self.screen.blit(score, (10, 10))
        self.screen.blit(enemy_fleet, (10, 30))

    def game_over(self):
        font = pygame.font.Font("freesansbold.ttf", 32)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        game_over = font.render("Game Over!", True, (r, g, b))
        restart = font.render("Press r to restart...", True, (r, g, b))
        self.screen.blit(game_over, (SCREEN_WIDTH / 2 - 32, 10))
        self.screen.blit(restart, (SCREEN_WIDTH / 2 - 32, 40))

    def create_enemy(self):
        sprite = pygame.image.load("sprites/spaceship_rot_180.png")
        p_w, p_h = sprite.get_rect().size
        enemy = Character()
        speed_X = random.randint(1, 3)
        speed_Y = random.randint(10, 30)
        enemy.set("enemyship", sprite, p_w, p_h, 0, 0, speed_X=speed_X, speed_Y=speed_Y)
        enemy.set_random_coordinated(SCREEN_MARGIN, SCREEN_WIDTH - SCREEN_MARGIN - enemy.sprite_w - 1, 50, 150)
        return enemy

    def exec(self):
        # Set the main loop
        running = True
        fire = False
        render = True
        rockdiv = self.player.sprite_w / self.rocket.sprite_w
        dx = 0
        dy = 0
        key_pressed = {"K_LEFT": False, "K_RIGHT": False}
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            # Player Movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -self.player.speed_X
                        key_pressed["K_LEFT"] = True
                    elif event.key == pygame.K_RIGHT:
                        dx = self.player.speed_X
                        key_pressed["K_RIGHT"] = True
                    elif event.key == pygame.K_SPACE:
                        fire = True
                    elif event.key == pygame.K_r:
                        render = True
                        self.score_value = 0
                        self.enemy = []
                        self.enemy_fleet = 1
                        for i in range(self.enemy_fleet):
                            self.enemy.append(self.create_enemy())

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        dx = 0
                        key_pressed["K_LEFT"] = False
                        if key_pressed["K_RIGHT"]:
                            dx = self.player.speed_X
                    elif event.key == pygame.K_RIGHT:
                        dx = 0
                        key_pressed["K_RIGHT"] = False
                        if key_pressed["K_LEFT"]:
                            dx = -self.player.speed_X

            if 5 <= self.player.coord_X <= SCREEN_WIDTH - SCREEN_MARGIN - self.player.sprite_w:
                self.player.move(dx=dx, dy=dy)
            elif self.player.coord_X <= SCREEN_MARGIN:
                self.player.coord_X = SCREEN_MARGIN
            elif self.player.coord_X >= SCREEN_WIDTH - SCREEN_MARGIN - self.player.sprite_w:
                self.player.coord_X = SCREEN_WIDTH - SCREEN_MARGIN - self.player.sprite_w

            if fire:
                self.rocket.coord_Y += self.rocket.speed_Y
                if self.rocket.coord_Y <= SCREEN_MARGIN:
                    fire = False
                    self.rocket.coord_X = self.player.coord_X + self.player.sprite_w / rockdiv + \
                                          self.rocket.sprite_w / 2
                    self.rocket.coord_Y = self.player.coord_Y + self.player.sprite_h / rockdiv
            else:
                self.rocket.coord_X = self.player.coord_X + self.player.sprite_w / rockdiv + self.rocket.sprite_w / 2
                self.rocket.coord_Y = self.player.coord_Y + self.player.sprite_h / rockdiv

            # Enemy Movement
            for i in range(self.enemy_fleet):
                self.enemy[i].coord_X += self.enemy[i].speed_X
                if SCREEN_WIDTH - SCREEN_MARGIN - self.enemy[i].sprite_w <= self.enemy[i].coord_X or \
                        SCREEN_MARGIN >= self.enemy[i].coord_X:
                    self.enemy[i].speed_X *= -1
                    self.enemy[i].coord_Y += self.enemy[i].speed_Y

                if isCollision(self.enemy[i].coord_X + self.enemy[i].sprite_w / 2,
                               self.enemy[i].coord_Y + self.enemy[i].sprite_h / 2,
                               self.player.coord_X + self.player.sprite_w / 2, self.player.coord_Y):
                    render = False

                if isCollision(self.enemy[i].coord_X + self.enemy[i].sprite_w / 2,
                               self.enemy[i].coord_Y + self.enemy[i].sprite_h / 2,
                               self.rocket.coord_X + self.rocket.sprite_w / 2, self.rocket.coord_Y):
                    fire = False
                    self.rocket.coord_X = self.player.coord_X + self.player.sprite_w / rockdiv + \
                                          self.rocket.sprite_w / 2
                    self.rocket.coord_Y = self.player.coord_Y + self.player.sprite_h / rockdiv
                    self.enemy[i].set_random_coordinated(SCREEN_MARGIN,
                                                         SCREEN_WIDTH - SCREEN_MARGIN - self.enemy[i].sprite_w - 1,
                                                         50, 150)
                    self.score_value += self.enemy_fleet
                    self.enemy_fleet += 1
                    self.enemy.append(self.create_enemy())

                self.enemy[i].draw(self.screen)
            if render:
                self.rocket.draw(self.screen)
                self.player.draw(self.screen)
            else:
                self.game_over()
            self.set_text_info()

            pygame.display.update()
            self.clock.tick(120)
