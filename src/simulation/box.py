import pygame
from . import settings as settings

class Box:
    
    def __init__(self, x, letter='A', color=(140, 200, 100), stacks=None):
        self.x = x
        self.y = 0
        self.vy = 0
        self.color = color
        self.landed = False
        self.letter = letter
        self.stacks = stacks or {}

    def update(self):
        if not self.landed and self.stacks:
            self.vy += settings.GRAVITY
            self.y += self.vy
            stack = self.stacks[self.x]
            ground_y = settings.GROUND_Y - len(stack) * settings.BOX_HEIGHT - settings.BOX_HEIGHT
            if self.y >= ground_y:
                self.y = ground_y
                self.landed = True
                stack.append(self)

    def draw(self, screen, font=None):
        rect = pygame.Rect(self.x - settings.BOX_WIDTH // 2, self.y, settings.BOX_WIDTH, settings.BOX_HEIGHT)

        shadow = rect.copy()
        shadow.move_ip(3, 3)
        pygame.draw.rect(screen, settings.SHADOW_COLOR, shadow, border_radius=12)

        pygame.draw.rect(screen, self.color, rect, border_radius=12)
        pygame.draw.rect(screen, settings.BORDER_COLOR, rect, 2, border_radius=12)

        if font:
            text = font.render(self.letter, True, settings.TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)