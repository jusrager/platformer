import pygame


class SceneWin:
    def __init__(self, SIZE, screen):
        self.screen = screen
        WIDTH, HEIGHT = SIZE
        path = 'background.png'
        image = pygame.image.load(path)
        self.img = pygame.transform.scale(image, (WIDTH, HEIGHT))
        self.width, self.height = (200, 80)
        self.X, self.Y = ((WIDTH - self.width) // 2, (HEIGHT - self.height) // 2 + 100)
        self.text_x, self.text_y = ((WIDTH - self.width) // 2 - 45, (HEIGHT - self.height) // 2 - 100)
        self.text_x1, self.text_y1 = ((WIDTH - self.width) // 2, (HEIGHT - self.height) // 2 - 25)
        self.text_x2, self.text_y2 = ((WIDTH - self.width) // 2 + 50, (HEIGHT - self.height) // 2 + 115)
        my_font = pygame.font.SysFont('Comic Sans MS', 35)
        my_font1 = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = my_font.render('Уровень пройден!', False, (0, 0, 0))
        self.text_surface1 = my_font1.render('Ваш результат:', False, (0, 0, 0))
        self.text_surface2 = my_font1.render('Ваш рекорд:', False, (0, 0, 0))
        self.text_surface3 = my_font1.render('Заново', False, (0, 0, 0))

    def update(self):
        self.screen.blit(self.img, (0, 0))
        pygame.draw.rect(self.screen, (54, 54, 54), [self.X - 5, self.Y - 5, self.width + 10, self.height + 10])
        pygame.draw.rect(self.screen, (204, 204, 204), [self.X, self.Y, self.width, self.height])
        self.screen.blit(self.text_surface, (self.text_x, self.text_y))
        self.screen.blit(self.text_surface1, (self.text_x, self.text_y1))
        self.screen.blit(self.text_surface2, (self.text_x, self.text_y1 + 45))
        self.screen.blit(self.text_surface3, (self.text_x2, self.text_y2))

    def render(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.X < event.pos[0] < self.X + self.width and self.Y < event.pos[1] < self.Y + self.height:
                print('game starts')
                return 2