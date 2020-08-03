import pygame, sys
from random import randrange


class Game:

    def __init__(self):
        pygame.init()
        self.ball_radius = 10
        self.ball_sp = 6
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.fps = 60
        self.FAKE_WIDTH = 1450
        self.WIDTH = 1200
        self.HEIGHT = 800
        self.win1 = pygame.display.set_mode((self.FAKE_WIDTH, self.HEIGHT))
        pygame.display.set_caption('ARCANOID')
        # , pygame.FULLSCREEN
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load('background2.jpg').convert()
        self.img2 = pygame.image.load('1.jpg').convert()
        self.f1 = pygame.font.Font(None, 36)
        self.score_font = pygame.font.SysFont('Calibri', 36)
        self.pause_font = pygame.font.SysFont('Calibri', 36)
        self.button_font = pygame.font.SysFont('Calibri', 36)
        self.score_1 = 0
        self.score = self.score_font.render(str(self.score_1), True, pygame.Color('green'))
        self.text1 = self.f1.render('Your score: ' + '0', 1, pygame.Color('green'))
        self.dx = 1
        self.dy = -1
        self.ball = pygame.Rect(randrange(self.ball_rect, self.WIDTH - self.ball_rect), int(self.HEIGHT // 1.5),
                                self.ball_rect, self.ball_rect)
        self.hit_rect = None
        self.hit_color = None
        self.block_list = [pygame.Rect(40 + 90 * i, 15 + 35 * j, 75, 30) for i in range(1) for j in range(1)]
        self.color_list = [(randrange(50, 256), randrange(50, 256), randrange(50, 256)) for i in range(12) for j in
                           range(10)]
        self.delta_x = None
        self.delta_y = None
        self.hit_index = None
        self.message = None
        self.font_win = pygame.font.SysFont('Arial', 36, bold=True)
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('background2.jpg').convert()
        self.platform()

    def detect_collision(self):
        if self.dx > 0:
            self.delta_x = self.rect.right - self.ball.left
        else:
            self.delta_x = self.ball.right - self.rect.left
        if self.dy > 0:
            self.delta_y = self.rect.bottom - self.ball.top
        else:
            self.delta_y = self.ball.bottom - self.rect.top
        if abs(self.delta_y - self.delta_x) < 10:
            self.dx, self.dy = - self.dx, - self.dy
        elif self.delta_x > self.delta_y:
            self.dy = - self.dy
        elif self.delta_y > self.delta_x:
            self.dx = - self.dx
        return self.dx, self.dy

    def platform(self):
        self.paddle_w = 150
        self.paddle_h = 30
        self.paddle_sp = 15
        self.paddle = pygame.Rect(self.WIDTH // 2 - self.paddle_w // 2, self.HEIGHT - self.paddle_h - 10,
                                  self.paddle_w, self.paddle_h)
        self.rect = pygame.draw.rect(self.win1, pygame.Color('yellow'), self.paddle)

    def collecting_score(self):
        self.text1 = self.f1.render(f'Your score: {self.score_1}', 1, pygame.Color('green'))

    def press_keyboard(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
            self.win1.blit(self.img, (0, 0))
            self.win1.blit(self.img2, (1203, 0))
            self.win1.blit(self.text1, (1210, 10))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.paddle.left > 0:
                self.paddle.left -= self.paddle_sp
            if keys[pygame.K_RIGHT] and self.paddle.right < self.WIDTH:
                self.paddle.right += self.paddle_sp
            if keys[pygame.K_SPACE]:
                self.pause()
                self.paddle_sp = 0
                self.ball_sp = 0
            [pygame.draw.rect(self.win1, self.color_list[color], block) for color, block in enumerate(self.block_list)]
            pygame.draw.rect(self.win1, pygame.Color('yellow'), self.paddle)
            pygame.draw.circle(self.win1, pygame.Color('red'), self.ball.center, self.ball_radius)
            self.ball.x += self.ball_sp * self.dx
            self.ball.y += self.ball_sp * self.dy
            if self.ball.centerx < self.ball_radius or self.ball.centerx > self.WIDTH - self.ball_radius:
                self.dx = - self.dx
            if self.ball.centery < self.ball_radius:
                self.dy = - self.dy
            if self.ball.colliderect(self.paddle) and self.dy > 0:
                self.dx, self.dy = self.dx, - self.dy
            self.hit_index = self.ball.collidelist(self.block_list)
            if self.hit_index != -1:
                self.hit_rect = self.block_list.pop(self.hit_index)
                self.hit_color = self.color_list.pop(self.hit_index)
                self.dx, self.dy = self.detect_collision()
                self.score_1 += 1
                self.collecting_score()
            if self.ball.bottom > self.HEIGHT:
                self.lose_screen()
                self.ball_sp = 0
                self.paddle_sp = 0
            elif not len(self.block_list):
                self.win_screen()
                self.ball_sp = 0
                self.paddle_sp = 0
            pygame.display.flip()
            self.clock.tick(self.fps)

    def pause(self):
        render = self.pause_font.render('PAUSE MODE', 1, (0, randrange(70, 120), 0))
        render2 = self.pause_font.render(f'YOUR CURRENT SCORE IS: {self.score_1}', 1, (0, randrange(70, 120), 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = self.WIDTH // 2, self.HEIGHT // 2
        pygame.draw.rect(self.win1, pygame.Color('black'), rect)
        self.win1.blit(render, (rect.centerx - 50, rect.centery - 120))
        self.win1.blit(render2, (rect.centerx - 50, rect.centery - 60))
        resume = self.button_font.render('RESUME', 1, pygame.Color('gray'))
        button_resume = pygame.Rect(0, 0, 200, 80)
        button_resume.center = self.WIDTH // 2, self.HEIGHT // 2 + 60
        pygame.draw.rect(self.win1, pygame.Color('White'), button_resume, border_radius=25, width=10)
        self.win1.blit(resume, (button_resume.centerx - 60, button_resume.centery - 15))
        pygame.display.flip()
        self.clock.tick(15)

    def win_screen(self):
        render = self.font_win.render('YOU WIN', 1, (0, randrange(70, 120), 0))
        render2 = self.font_win.render(f'YOUR SCORE IS: {self.score_1}', 1, (0, randrange(70, 120), 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = self.WIDTH // 2, self.HEIGHT // 2
        pygame.draw.rect(self.win1, pygame.Color('black'), rect)
        self.win1.blit(render, (rect.centerx - 50, rect.centery - 100))
        self.win1.blit(render2, (rect.centerx - 50, rect.centery - 60))
        pygame.display.flip()
        self.clock.tick(15)

    def lose_screen(self):
        render = self.font_win.render('YOU LOST', 1, (0, randrange(70, 120), 0))
        render2 = self.font_win.render(f'YOUR SCORE IS: {self.score_1}', 1, (0, randrange(70, 120), 0))
        rect = pygame.Rect(0, 0, 1000, 300)
        rect.center = self.WIDTH // 2, self.HEIGHT // 2
        pygame.draw.rect(self.win1, pygame.Color('black'), rect)
        self.win1.blit(render, (rect.centerx - 50, rect.centery - 100))
        self.win1.blit(render2, (rect.centerx - 50, rect.centery - 60))
        pygame.display.flip()
        self.clock.tick(15)

    def menu(self):
        x = 0
        button_font = pygame.font.SysFont('Calibri', 36)
        label_font = pygame.font.SysFont('Calibri', 270)
        start = button_font.render('START', 1, pygame.Color('gray'))
        button_start = pygame.Rect(0, 0, 200, 85)
        button_start.center = self.WIDTH // 2, self.HEIGHT // 2 - 100
        exit = button_font.render('EXIT', 1, pygame.Color('gray'))
        button_exit = pygame.Rect(0, 0, 200, 85)
        button_exit.center = self.WIDTH // 2, self.HEIGHT // 2 + 20

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.win1.blit(self.menu_picture, (0, 0), (x % self.WIDTH, self.HEIGHT//10, self.WIDTH + 500, self.HEIGHT))
            x += 1

            pygame.draw.rect(self.win1, pygame.Color('Black'), button_start, border_radius=25, width=10)
            self.win1.blit(start, (button_start.centerx - 45, button_start.centery - 17))

            pygame.draw.rect(self.win1, pygame.Color('Black'), button_exit, border_radius=25, width=10)
            self.win1.blit(exit, (button_exit.centerx - 35, button_exit.centery - 15))

            color = randrange(130)
            label = label_font.render('ARCANOID', 1, (color, 191, color))
            self.win1.blit(label, (18, -10))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.win1, pygame.Color('Black'), button_start, border_radius=25, width=10)
                self.win1.blit(start, (button_start.centerx - 45, button_start.centery - 17))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.win1, pygame.Color('Black'), button_exit, border_radius=25, width=10)
                self.win1.blit(exit, (button_exit.centerx - 35, button_exit.centery - 15))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(15)


A = Game()
A.menu()
A.press_keyboard()
A.detect_collision()
