class Scene1:
    def __init__(self):
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect((WIDTH - 160) // 2 - 20, (HEIGHT - 32) // 2 - 35, 160, 32)
        color_inactive = pygame.Color('lightslategrey')
        color_active = pygame.Color('lightskyblue')
        color = color_inactive
        active = False
        error = False
        text = ''