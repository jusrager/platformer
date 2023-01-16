import pygame


class Scene1:
    def __init__(self, SIZE, screen):
        self.screen = screen
        WIDTH, HEIGHT = SIZE
        self.width, self.height = (200, 80)
        self.X, self.Y = ((WIDTH - self.width) // 2, (HEIGHT - self.height) // 2)
        self.text_x, self.text_y = ((WIDTH - self.width) // 2 + 10, (HEIGHT - self.height) // 2 - 100)
        self.text_x1, self.text_y1 = ((WIDTH - self.width) // 2 + 44, (HEIGHT - self.height) // 2 + 16)
        self.text_x2, self.text_y2 = ((WIDTH - self.width) // 2 - 104, (HEIGHT - self.height) // 2 + 124)
        my_font = pygame.font.SysFont('Comic Sans MS', 35)
        my_font1 = pygame.font.SysFont('Comic Sans MS', 30)
        my_font2 = pygame.font.SysFont('Comic Sans MS', 23)
        self.font = pygame.font.Font(None, 32)
        self.input_box = pygame.Rect((WIDTH - 160) // 2 - 20, (HEIGHT - 32) // 2 - 35, 160, 32)
        self.color_inactive = pygame.Color('lightslategrey')
        self.color_active = pygame.Color('lightskyblue')
        self.color = self.color_inactive
        self.active = False
        self.error = False
        self.text = ''
        path = 'background.png'
        image = pygame.image.load(path)
        self.img = pygame.transform.scale(image, (WIDTH, HEIGHT))
        self.txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, self.txt_surface.get_width() + 10)
        self.input_box.w = width
        self.text_surface3 = my_font.render('Введите логин', False, (0, 0, 0))
        self.text_surface4 = my_font1.render('OK', False, (0, 0, 0))
        self.text_surface5 = my_font2.render('Введите логин! 8 букв, латиница', False, (247, 19, 24))

    def update(self):
        self.screen.blit(self.img, (0, 0))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        pygame.draw.rect(self.screen, (54, 54, 54), [self.X - 5, self.Y + 35, self.width + 10, self.height + 10])
        pygame.draw.rect(self.screen, (204, 204, 204), [self.X, self.Y + 40, self.width, self.height])
        self.screen.blit(self.txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        self.screen.blit(self.text_surface3, (self.text_x - 37, self.text_y))
        self.screen.blit(self.text_surface4, (self.text_x1 + 30, self.text_y1 + 40))
        if self.error:
            self.screen.blit(self.text_surface5, (self.text_x2 + 20, self.text_y2 + 15))

    def render(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
            if self.X < event.pos[0] < self.X + self.width and self.Y + 40 < event.pos[1] < self.Y + self.height + 40:
                print('click')
                if len(self.text) < 8:
                    self.error = True
                else:
                    return (2, self.text)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 8:
                        self.text += event.unicode
        self.txt_surface = self.font.render(self.text, True, self.color)
        return False
