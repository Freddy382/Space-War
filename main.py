import pygame
import random
import sys

class BULLET():
    def __init__(self, width, height, bullet_width, bullet_height):
        self.x_pos = width
        self.y_pos = random.randint(0, height - bullet_height)

        self.bullet_width = bullet_width
        self.bullet_height = bullet_height

        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.bullet_width, self.bullet_height)

    def draw_bullet(self):
        pygame.draw.rect(screen, BLUE, self.rect)

    def move_bullet(self):
        self.rect.x -= 8

class PLAYER():

    def __init__(self, width, height, player_width, player_height):
        self.width = width
        self.height = height

        self.player_width = player_width
        self.player_height = player_height

        self.x_pos = random.randint(0, self.width - self.player_width)
        self.y_pos = random.randint(0, self.height - self.player_height)

        self.image = pygame.image.load("./assets/player.png")
        self.small_image = pygame.transform.scale(self.image, (50, 50))

        self.rotated = pygame.transform.rotate(self.small_image, 90)

        self.rect = self.rotated.get_rect()

        self.rect.x = self.width / 2 - 25
        self.rect.y = self.height / 2 - 25

    def draw_player(self):
        screen.blit(self.rotated, self.rect)

class MAIN():
    def __init__(self):
        self.player = PLAYER(width, height, 50, 50)
        self.bullet_counter = 0

        self.lives = 3
        self.font = pygame.font.Font("./assets/pixel.ttf", 25)
        self.x = 0

        self.tick_counter = 0
        self.seconds = 0

        self.bullets = {}

    def game_manager(self):
        self.move_background()
        self.draw_bullet_objects()
        self.move_bullet_objects()
        self.player.draw_player()
        self.remove_bullets()
        self.draw_font()
        self.on_bullet_collision()
        self.change_counter()
        self.is_colliding()

        if self.tick_counter % 30 == 0:
            self.create_bullets()

    def move_background(self):
        rel_x = self.x % BG.get_rect().width
        screen.blit(BG, (rel_x - BG.get_rect().width, 0))
        if rel_x < width:
            screen.blit(BG, (rel_x, 0))
        self.x -= 10

    def create_bullets(self):
        self.bullets[self.bullet_counter] = BULLET(width, height, 20, 10)
        self.bullet_counter += 1

    def draw_bullet_objects(self):
        for bullet_object in self.bullets.values():
            pygame.draw.rect(screen, RED, bullet_object.rect)

    def draw_font(self):
        lives = self.font.render(f"Lives: {self.lives}", False, WHITE)
        screen.blit(lives, (0, 0))

        seconds = self.font.render(f"Seconds: {self.seconds}", False, WHITE)
        screen.blit(seconds, (width - seconds.get_rect().width, 0))

    def move_bullet_objects(self):
        for bullet_object in self.bullets.values():
            bullet_object.move_bullet()

    def remove_bullets(self):
        for key, value in list(self.bullets.items()):
            if value.x_pos <= 0 - value.bullet_width:
                del self.bullets[key]

    def is_colliding(self):
        for key, value in list(self.bullets.items()):
            if value.rect.colliderect(main.player.rect):
                del self.bullets[key]
                return True

    def on_bullet_collision(self):
        if self.is_colliding():
            self.lives -= 1

    def game_over(self):
        if not self.lives == 0:
            return False
        else:
            return True

    def change_counter(self):
        self.tick_counter += 1
        if self.tick_counter % FPS == 0:
            self.seconds += 1

    def reset(self):
        self.lives = 3
        self.bullet_counter = 0
        self.bullets.clear()
        self.x = 0
        self.seconds = 0
        self.tick_counter = 0

class GAMESTATE():
    def __init__(self):
        self.state = "intro"
        self.font = pygame.font.Font("./assets/pixel.ttf", 25)

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state = "main_game"

        screen.blit(BG, (0, 0))

        start_info = self.font.render("SPACE WAR", True, WHITE)
        screen.blit(start_info, (width / 2 - start_info.get_rect().width / 2, height / 2))

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and main.player.rect.x >= 0:

            main.player.rect.x -= vel

        elif keys[pygame.K_RIGHT] and main.player.rect.x <= width - main.player.player_width:
            main.player.rect.x += vel

        elif keys[pygame.K_UP] and main.player.rect.y >= 0:
            main.player.rect.y -= vel

        elif keys[pygame.K_DOWN] and main.player.rect.y <= height - main.player.player_height:
            main.player.rect.y += vel

        pygame.time.set_timer(keys[pygame.K_v], 0)

        main.game_manager()

        if main.game_over():
            self.state = "endscreen"

    def endscreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                main.reset()
                self.state = "main_game"

        screen.blit(BG, (0, 0))

        font_text = self.font.render("GAME OVER", True, WHITE)
        screen.blit(font_text, (width / 2 - 65, height / 2 - 10))

    def state_manager(self):
        if self.state == "intro":
            self.intro()

        elif self.state == "main_game":
            self.main_game()

        elif self.state == "endscreen":
            self.endscreen()

pygame.init()

width, height = 500, 500

screen = pygame.display.set_mode([width, height])

BG = pygame.image.load("./assets/BG.png")
ICON = pygame.image.load("./assets/player.png")

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

FPS = 60
vel = 10

clock = pygame.time.Clock()

bullet = BULLET(width, height, 20, 10)

main = MAIN()
game_state = GAMESTATE()

pygame.display.set_caption("Space War")
pygame.display.set_icon(ICON)

run = True

while run:

    #pygame.time.delay(100)

    game_state.state_manager()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()



