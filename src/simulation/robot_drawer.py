import pygame
from . import settings

class RobotDrawer:
        
    def draw(self, screen, x, y, box):
        
        pygame.draw.line(screen, settings.BORDER_COLOR, (0, settings.GROUND_Y), (settings.WIDTH, settings.GROUND_Y), 3)
        base_rect = pygame.Rect(x - 30, 50, 60, 20)
        pygame.draw.rect(screen, (100, 100, 100), base_rect, border_radius=5)

        arm_rect = pygame.Rect(x - 10, 70, 20, y - 70)
        pygame.draw.rect(screen, (70, 70, 70), arm_rect, border_radius=5)

        grip_y = y
        grip_width = 60
        grip_height = 15
        grip_rect = pygame.Rect(x - grip_width // 2, grip_y, grip_width, grip_height)
        pygame.draw.rect(screen, (50, 50, 50), grip_rect, border_radius=5)

        finger_width = 10
        finger_height = grip_height
        left_finger = pygame.Rect(x - grip_width // 2, grip_y, finger_width, finger_height)
        right_finger = pygame.Rect(x + grip_width // 2 - finger_width, grip_y, finger_width, finger_height)
        pygame.draw.rect(screen, (80, 80, 80), left_finger, border_radius=3)
        pygame.draw.rect(screen, (80, 80, 80), right_finger, border_radius=3)

        if box:
            box.draw(screen, None)