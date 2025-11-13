import pygame
from pygame import *

pygame.init()

BG_COLOR = (200, 255, 255)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Ping Pong")
window.fill(BG_COLOR)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < WINDOW_HEIGHT - 150:
            self.rect.y += self.speed

    def move_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < WINDOW_HEIGHT - 150:
            self.rect.y += self.speed


left_paddle = Player('paddle.png', 30, 200, 6, 50, 150)
right_paddle = Player('paddle.png', 520, 200, 6, 50, 150)
ball = GameSprite('ball.png', 300, 250, 4, 50, 50)

ball_speed_x = 3
ball_speed_y = 3

font.init()
game_font = font.Font(None, 50)
lose_left = game_font.render('Left Player Loses!', True, (180, 0, 0))
lose_right = game_font.render('Right Player Loses!', True, (180, 0, 0))
restart_text = game_font.render('Press SPACE to Restart', True, (0, 100, 180))

clock = time.Clock()
FPS = 60
game = True
finish = False

def reset_game():
    global finish, ball_speed_x, ball_speed_y
    finish = False
    ball.rect.x = 300
    ball.rect.y = 250
    ball_speed_x = 3
    ball_speed_y = 3
    left_paddle.rect.y = 200
    right_paddle.rect.y = 200

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and finish:
                reset_game()

    if not finish:
        window.fill(BG_COLOR)

        left_paddle.move_left()
        right_paddle.move_right()

        ball.rect.x += ball_speed_x
        ball.rect.y += ball_speed_y

        if ball.rect.y <= 0 or ball.rect.y >= WINDOW_HEIGHT - 50:
            ball_speed_y *= -1

        if sprite.collide_rect(left_paddle, ball) or sprite.collide_rect(right_paddle, ball):
            ball_speed_x *= -1

        if ball.rect.x < 0:
            finish = True
            window.blit(lose_left, (150, 200))
            window.blit(restart_text, (100, 270))
        elif ball.rect.x > WINDOW_WIDTH:
            finish = True
            window.blit(lose_right, (150, 200))
            window.blit(restart_text, (100, 270))

        left_paddle.reset()
        right_paddle.reset()
        ball.reset()
    else:
        window.blit(restart_text, (100, 270))

    display.update()
    clock.tick(FPS)

pygame.quit()
