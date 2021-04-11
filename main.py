import pygame
import random
import sys
import json
import numpy

class PARTICLES():
    def __init__(self):
        self.particles = []

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0][0] += particle[2][0]
                particle[0][1] += particle[2][1]
                particle[1] -= 0.2
                pygame.draw.circle(screen, particle[3], particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = main.player.rect.x - 5
        pos_y = random.randint(main.player.rect.y, main.player.rect.y + main.player.player_height)
        radius = 5
        direction_x = -3
        direction_y = random.randint(-1, 1)
        color = random.choice([RED, ORANGE])

        particle_circle = [[pos_x, pos_y], radius, [direction_x, direction_y], color]

        self.particles.append(particle_circle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0 and particle[0][0] <= main.player.rect.x]
        self.particles = particle_copy

class BULLET():
    def __init__(self, width, height, bullet_width, bullet_height):
        self.x_pos = width
        self.y_pos = random.randint(0, height - bullet_height)

        self.bullet_width = bullet_width
        self.bullet_height = bullet_height

        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.bullet_width, self.bullet_height)

    def draw_bullet(self):
        pygame.draw.rect(screen, GREEN, self.rect)

    def move_bullet(self, spawn_speed):
        self.rect.x -= spawn_speed

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

        self.velocity = 5

    def draw_player(self):
        screen.blit(self.rotated, (self.rect.x, self.rect.y))

class MAIN():
    def __init__(self):
        self.player = PLAYER(width, height, 50, 50)
        self.particles = PARTICLES()

        self.bullet_counter = 0

        self.lives = 3
        self.font = pygame.font.Font("./assets/pixel.ttf", 25)
        self.x = 0

        self.lives_color = WHITE
        self.lives_reset_timer = 0

        self.bullet_velocity = 5
        self.difficulty = "MEDIUM"

        self.music = True

        self.highscore = int

        self.frames_counter = 0
        self.spawn_rate = 50

        self.score = 0

        self.sound = pygame.mixer.Sound("./assets/laser.mp3")

        self.bullets = {}

    def game_manager(self):
        self.move_background()
        self.draw_bullet_objects()
        self.move_bullet_objects()
        self.player.draw_player()
        self.remove_bullets()
        self.change_frames_counter()
        self.create_bullets()
        self.draw_font()
        self.on_bullet_collision()
        self.is_colliding()
        self.update_highscore()

        self.particles.emit()

    def move_background(self):
        rel_x = self.x % BG.get_rect().width
        screen.blit(BG, (rel_x - BG.get_rect().width, 0))
        if rel_x < width:
            screen.blit(BG, (rel_x, 0))
        self.x -= 10

    def create_bullets(self):
        if self.frames_counter % self.spawn_rate == 0:
            self.bullets[self.bullet_counter] = BULLET(width, height, 20, 5)
            self.bullet_counter += 1
            self.frames_counter = 0

    def draw_bullet_objects(self):
        for bullet_object in self.bullets.values():
            bullet_object.draw_bullet()

    def draw_font(self):
        lives = self.font.render(f"LIVES: {self.lives}", False, self.lives_color)
        screen.blit(lives, (0, 0))

        seconds = self.font.render(f"SCORE: {self.score}", False, WHITE)
        screen.blit(seconds, (width - seconds.get_rect().width, 0))

    def move_bullet_objects(self):
        for bullet_object in self.bullets.values():
            bullet_object.move_bullet(self.bullet_velocity)

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
        self.lives_reset_timer += 1

        if self.is_colliding():
            self.lives_reset_timer = 0
            self.lives -= 1
            self.lives_color = RED

            if self.music:
                self.sound.play()

        else:
            if self.lives_reset_timer % 60 == 0:
                self.lives_color = WHITE
                self.lives_reset_timer = 0

    def game_over(self):
        if not self.lives == 0:
            return False
        else:
            return True

    def change_counter(self):
         self.score += 1

    def change_frames_counter(self):
        self.frames_counter += 1

    def change_spawn_rate(self):
        if self.spawn_rate >= 11:
            self.spawn_rate -= 5

    def update_highscore(self):
        if self.game_over():
            if self.score >= int(self.highscore):
                with open("highscore.json", "r") as f:
                    data = json.load(f)
                    data["highscore"] = self.score

                with open("highscore.json", "w") as f:
                    json.dump(data, f, indent=4)

    def reset(self):
        self.lives = 3
        self.bullet_counter = 0
        self.bullets.clear()
        self.x = 0
        self.score = 0
        self.spawn_rate = 50

class GAMESTATE():
    def __init__(self):
        self.state = "intro"

        self.big_font = pygame.font.Font("./assets/pixel.ttf", 25)
        self.small_font = pygame.font.Font("./assets/pixel.ttf", 15)

        self.sound = pygame.mixer.Sound("./assets/click.mp3")

        self.difficulty_text = self.big_font.render("MEDIUM", True, WHITE)
        self.music_text = self.small_font.render("SOUND ON", True, WHITE)

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if width / 2 - self.difficulty_text.get_width() <= mouse_pos[0] and height / 2 + 100 <= mouse_pos[1] and width / 2 + self.difficulty_text.get_width() / 2 >= mouse_pos[0] and mouse_pos[1] <= height / 2 + 100 + self.difficulty_text.get_height() / 2:

                    if main.difficulty == "MEDIUM":
                        main.difficulty = "HARD"
                        main.bullet_velocity = 12

                    elif main.difficulty == "HARD":
                        main.difficulty = "EASY"
                        main.bullet_velocity = 5

                    else:
                        main.difficulty = "MEDIUM"
                        main.bullet_velocity = 8

                elif width - 20 - self.music_text.get_width() <= mouse_pos[0] and height - 20 - self.music_text.get_height() <= mouse_pos[1]:
                    if not main.music:
                        main.music = True
                    else:
                        main.music = False

                    if main.music:
                        self.music_text = self.small_font.render("SOUND: ON", True, WHITE)

                    else:
                        self.music_text = self.small_font.render("SOUND: OFF", True, WHITE)

                else:
                    self.state = "main_game"

                if main.music:
                    self.sound.play()

        screen.blit(BG, (0, 0))

        if width / 2 - self.difficulty_text.get_width() <= mouse_pos[0] and height / 2 + 100 <= mouse_pos[1] and width / 2 + self.difficulty_text.get_width() / 2 >= mouse_pos[0] and mouse_pos[1] <= height / 2 + 100 + self.difficulty_text.get_height() / 2:
            self.difficulty_text = self.big_font.render(main.difficulty, True, BLUE)
        else:
            self.difficulty_text = self.big_font.render(main.difficulty, True, WHITE)

        if width - 20 - self.music_text.get_width() <= mouse_pos[0] and height - 20 - self.music_text.get_height() <= mouse_pos[1]:
            if main.music:
                self.music_text = self.small_font.render("SOUND: ON", True, BLUE)
            else:
                self.music_text = self.small_font.render("SOUND: OFF", True, BLUE)
        else:
            if main.music:
                self.music_text = self.small_font.render("SOUND: ON", True, WHITE)
            else:
                self.music_text = self.small_font.render("SOUND: OFF", True, WHITE)


        space_font = pygame.font.Font("./assets/pixel.ttf", 40)
        start_info = space_font.render("SPACE WAR", True, WHITE)

        screen.blit(self.difficulty_text, (width / 2 - self.difficulty_text.get_width() / 2, height / 2 + 100))
        screen.blit(self.music_text, (width - self.music_text.get_width() - 20, height - self.music_text.get_height() - 20))
        screen.blit(start_info, (width / 2 - start_info.get_rect().width / 2, height / 2 - 40))

        with open("highscore.json", "r") as f:
            data = json.load(f)

            highscore_font = self.small_font
            main.highscore = data["highscore"]

            highscore_text = highscore_font.render(f"HIGHSCORE: {main.highscore}", True, WHITE)
            screen.blit(highscore_text, (width / 2 - start_info.get_rect().width / 2 + 45, height / 2 + 20))

            screen.blit(main.player.small_image, (width / 2 - main.player.small_image.get_rect().width / 2 - 180, height / 2))
            screen.blit(main.player.small_image, (width / 2 - main.player.small_image.get_rect().width / 2 + 180, height / 2))

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == counter_increase_event:
                main.change_counter()

            elif event.type == spawn_rate_increase_event:
                main.change_spawn_rate()

            elif event.type == particle_spawn_event:
                main.particles.add_particles()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and main.player.rect.x >= 0:
            main.player.rect.x -= main.player.velocity

        elif keys[pygame.K_RIGHT] and main.player.rect.x <= width - main.player.player_width:
            main.player.rect.x += main.player.velocity

        elif keys[pygame.K_UP] and main.player.rect.y >= 0:
            main.player.rect.y -= main.player.velocity

        elif keys[pygame.K_DOWN] and main.player.rect.y <= height - main.player.player_height:
            main.player.rect.y += main.player.velocity

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
                self.state = "intro"
                if main.music:
                    self.sound.play()

        screen.blit(BG, (0, 0))

        end_font_text = self.big_font.render("GAME OVER", True, WHITE)
        score_text = self.small_font.render(f"YOUR SCORE: {main.score}", True, WHITE)

        screen.blit(end_font_text, (width / 2 - 65, height / 2 - 10))
        screen.blit(score_text, (width / 2 - 55, height / 2 + 50))

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

pygame.display.set_caption("Space War")
pygame.display.set_icon(ICON)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

FPS = 60


clock = pygame.time.Clock()

main = MAIN()
game_state = GAMESTATE()

counter_increase_event = pygame.USEREVENT + 1
pygame.time.set_timer(counter_increase_event, 1000)

spawn_rate_increase_event = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_rate_increase_event, 10000)

particle_spawn_event = pygame.USEREVENT + 3
pygame.time.set_timer(particle_spawn_event, 50)

while True:

    mouse_pos = pygame.mouse.get_pos()

    game_state.state_manager()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()



