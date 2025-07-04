import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Arm Box Stacking")

# Colors
WHITE = (240, 240, 240)
BORDER_COLOR = (50, 50, 50)
SHADOW_COLOR = (180, 180, 180)
TEXT_COLOR = (30, 30, 30)
COLOR_LIST = [
    (255, 140, 140), (140, 255, 140), (140, 140, 255),
    (255, 215, 140), (200, 140, 255), (140, 255, 255)
]

# Constants
FPS = 60
GRAVITY = 0.4
BOX_WIDTH, BOX_HEIGHT = 100, 50
STACK_X_POSITIONS = [200, 350, 500]
GROUND_Y = HEIGHT - 20

# State
stacks = {x: [] for x in STACK_X_POSITIONS}
falling_boxes = []

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)
label_font = pygame.font.SysFont("Arial", 20, bold=False)  # For stack labels

class Box:
    def __init__(self, x, letter='A', color=(140, 200, 100)):
        self.x = x
        self.y = 0
        self.vy = 0
        self.color = color
        self.landed = False
        self.letter = letter

    def update(self):
        if not self.landed:
            self.vy += GRAVITY
            self.y += self.vy
            stack = stacks[self.x]
            ground_y = GROUND_Y - len(stack) * BOX_HEIGHT - BOX_HEIGHT
            if self.y >= ground_y:
                self.y = ground_y
                self.landed = True
                stack.append(self)

    def draw(self, screen):
        rect = pygame.Rect(self.x - BOX_WIDTH // 2, self.y, BOX_WIDTH, BOX_HEIGHT)

        # Shadow
        shadow = rect.copy()
        shadow.move_ip(5, 5)
        pygame.draw.rect(screen, SHADOW_COLOR, shadow, border_radius=12)

        # Box
        pygame.draw.rect(screen, self.color, rect, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2, border_radius=12)

        # Letter
        text = font.render(self.letter, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

class RobotArm:
    def __init__(self):
        self.robot_x = STACK_X_POSITIONS[0]
        self.robot_y = 100  # initial height
        self.speed = 8
        self.state = "idle"  # idle, moving_to_pick, picking, lifting, moving_to_place, lowering, releasing
        self.box = None
        self.from_x = None
        self.to_x = None
        self.target_y = None

    def start_move(self, from_x, to_x):
        if self.state == "idle":
            if not stacks[from_x]:
                print(f"No box to pick in column {from_x}")
                return False
            self.from_x = from_x
            self.to_x = to_x
            self.box = stacks[from_x].pop()
            self.box.landed = False
            self.state = "moving_to_pick"
            self.target_y = self._get_stack_top_y(from_x) - BOX_HEIGHT - 20
            print(f"Robot started moving from {from_x} to {to_x}")
            return True
        return False

    def _get_stack_top_y(self, x):
        return GROUND_Y - len(stacks[x]) * BOX_HEIGHT

    def update(self):
        if self.state == "idle":
            return

        if self.state == "moving_to_pick":
            target_x = self.from_x
            if abs(self.robot_x - target_x) > self.speed:
                self.robot_x += self.speed if self.robot_x < target_x else -self.speed
            else:
                self.robot_x = target_x
                self.state = "picking"
            return

        if self.state == "picking":
            if self.robot_y < self.target_y:
                self.robot_y += self.speed
            else:
                self.robot_y = self.target_y
                self.state = "lifting"
            return

        if self.state == "lifting":
            if self.robot_y > 100:
                self.robot_y -= self.speed
                self.box.y = self.robot_y + 20
                self.box.x = self.robot_x
            else:
                self.robot_y = 100
                self.state = "moving_to_place"
            return

        if self.state == "moving_to_place":
            target_x = self.to_x
            if abs(self.robot_x - target_x) > self.speed:
                direction = self.speed if self.robot_x < target_x else -self.speed
                self.robot_x += direction
                self.box.x = self.robot_x
                self.box.y = self.robot_y + 20
            else:
                self.robot_x = target_x
                self.state = "lowering"
                self.target_y = self._get_stack_top_y(self.to_x) - BOX_HEIGHT - 20
            return

        if self.state == "lowering":
            if self.robot_y < self.target_y:
                self.robot_y += self.speed
                self.box.y = self.robot_y + 20
                self.box.x = self.robot_x
            else:
                self.robot_y = self.target_y
                self.state = "releasing"
            return

        if self.state == "releasing":
            self.box.vy = 0
            falling_boxes.append(self.box)
            self.box = None
            self.state = "idle"
            self.from_x = None
            self.to_x = None

    def draw(self, screen):
        base_rect = pygame.Rect(self.robot_x - 30, 50, 60, 20)
        pygame.draw.rect(screen, (100, 100, 100), base_rect, border_radius=5)

        arm_rect = pygame.Rect(self.robot_x - 10, 70, 20, self.robot_y - 70)
        pygame.draw.rect(screen, (70, 70, 70), arm_rect, border_radius=5)

        grip_y = self.robot_y
        grip_width = 60
        grip_height = 15
        grip_rect = pygame.Rect(self.robot_x - grip_width // 2, grip_y, grip_width, grip_height)
        pygame.draw.rect(screen, (50, 50, 50), grip_rect, border_radius=5)

        finger_width = 10
        finger_height = grip_height
        left_finger = pygame.Rect(self.robot_x - grip_width // 2, grip_y, finger_width, finger_height)
        right_finger = pygame.Rect(self.robot_x + grip_width // 2 - finger_width, grip_y, finger_width, finger_height)
        pygame.draw.rect(screen, (80, 80, 80), left_finger, border_radius=3)
        pygame.draw.rect(screen, (80, 80, 80), right_finger, border_radius=3)

        if self.box:
            self.box.draw(screen)

def spawn_initial_boxes():
    letters = ['A', 'B', 'C', 'D', 'E']
    random.shuffle(letters)
    # Pick distinct colors for boxes without repetition
    used_colors = []
    for letter in letters:
        available_colors = [c for c in COLOR_LIST if c not in used_colors]
        color = random.choice(available_colors)
        used_colors.append(color)
        box = Box(STACK_X_POSITIONS[0], letter=letter, color=color)
        falling_boxes.append(box)

def draw_stack_labels():
    labels = ["Stack 1", "Stack 2", "Stack 3"]
    for x, label in zip(STACK_X_POSITIONS, labels):
        text = label_font.render(label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(x, GROUND_Y + 30))  # Below ground line
        screen.blit(text, text_rect)

# Spawn initial boxes
spawn_initial_boxes()

robot = RobotArm()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if robot.state != "idle":
                continue
            if event.key == pygame.K_q:
                robot.start_move(STACK_X_POSITIONS[0], STACK_X_POSITIONS[1])
            elif event.key == pygame.K_w:
                robot.start_move(STACK_X_POSITIONS[0], STACK_X_POSITIONS[2])
            elif event.key == pygame.K_e:
                robot.start_move(STACK_X_POSITIONS[1], STACK_X_POSITIONS[2])
            elif event.key == pygame.K_r:
                robot.start_move(STACK_X_POSITIONS[2], STACK_X_POSITIONS[1])
            elif event.key == pygame.K_t:
                robot.start_move(STACK_X_POSITIONS[1], STACK_X_POSITIONS[0])
            elif event.key == pygame.K_y:
                robot.start_move(STACK_X_POSITIONS[2], STACK_X_POSITIONS[0])
            elif event.key == pygame.K_j:
                print("Robot arm is idle, no action taken.")

    # Update robot arm
    robot.update()

    # Update falling boxes
    for box in falling_boxes[:]:
        box.update()
        box.draw(screen)
        if box.landed:
            falling_boxes.remove(box)

    # Draw stacked boxes
    for x in stacks:
        for box in stacks[x]:
            box.draw(screen)

    # Draw robot
    robot.draw(screen)

    # Draw stack labels below columns
    draw_stack_labels()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
