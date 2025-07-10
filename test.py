import pygame
import sys
import random
import socket
import threading
import re

pygame.init()  # Initialize all imported pygame modules

# Screen setup
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create display window
pygame.display.set_caption("Blockworld Simulation")  # Set window title

# Colors (RGB tuples)
WHITE = (240, 240, 240)
BORDER_COLOR = (50, 50, 50)
SHADOW_COLOR = (180, 180, 180)
TEXT_COLOR = (30, 30, 30)
# List of colors to assign randomly to boxes
COLOR_LIST = [
    (255, 140, 140), (140, 255, 140), (140, 140, 255),
    (255, 215, 140), (200, 140, 255), (140, 255, 255)
]

# Constants
FPS = 60  # Frames per second for smooth animation
GRAVITY = 0.4  # Gravity force applied to falling boxes
BOX_WIDTH, BOX_HEIGHT = 100, 50  # Size of each box
STACK_X_POSITIONS = [200, 350, 500]  # X positions of the three stacks
GROUND_Y = HEIGHT - 50  # Y position of the ground level

# State containers for boxes
stacks = {x: [] for x in STACK_X_POSITIONS}  # Dictionary: stack x-position -> list of boxes stacked there
falling_boxes = []  # List of boxes currently falling

clock = pygame.time.Clock()  # Used to control frame rate
font = pygame.font.SysFont("Arial", 28, bold=True)  # Font for letters on boxes
label_font = pygame.font.SysFont("Arial", 20, bold=False)  # Font for stack labels

# Class to represent each individual box
class Box:
    def __init__(self, x, letter='A', color=(140, 200, 100)):
        self.x = x  # Horizontal position of the box (center)
        self.y = 0  # Vertical position of the box (top)
        self.vy = 0  # Vertical velocity for falling
        self.color = color  # Box color
        self.landed = False  # Whether box has landed on a stack or ground
        self.letter = letter  # Letter displayed on the box

    def update(self):
        # Update box position if it's still falling
        if not self.landed:
            self.vy += GRAVITY  # Accelerate downward by gravity
            self.y += self.vy  # Apply vertical velocity

            # Calculate the Y coordinate of the top of the stack it is falling on
            stack = stacks[self.x]
            ground_y = GROUND_Y - len(stack) * BOX_HEIGHT - BOX_HEIGHT

            # If box reached or passed the ground/stack top, snap it into place
            if self.y >= ground_y:
                self.y = ground_y
                self.landed = True  # Mark box as landed
                stack.append(self)  # Add box to appropriate stack

    def draw(self, screen):
        # Draw the box with shadow and border

        # Rectangle representing box position and size
        rect = pygame.Rect(self.x - BOX_WIDTH // 2, self.y, BOX_WIDTH, BOX_HEIGHT)

        # Draw the colored box with rounded corners
        pygame.draw.rect(screen, self.color, rect, border_radius=12)

        # Draw a dark border around the box
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2, border_radius=12)

        # Render the letter on the box, centered
        text = font.render(self.letter, True, TEXT_COLOR)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)  # Draw the letter on the box

# Class representing the robot arm that moves boxes between stacks
class RobotArm:
    def __init__(self):
        self.robot_x = STACK_X_POSITIONS[0]  # Current horizontal position of the robot arm
        self.robot_y = 100  # Current vertical position (height) of the robot arm's gripper
        self.speed = 8  # Speed of robot arm movements
        self.state = "idle"  # Current state of the robot arm (idle, moving, picking, etc.)
        self.box = None  # Box currently held by the robot arm (if any)
        self.from_x = None  # Starting stack x-position for the move
        
        # target to move the box to 
        self.to_x = None  # Target stack x-position for the move
        self.target_y = None  # Target vertical position for lowering/raising the arm

    # Start moving a box from from_x stack to to_x stack
    def start_move(self, from_x, to_x):
        # Only start if robot is idle and from_x stack is not empty
        if self.state == "idle":
            if not stacks[from_x]:
                print(f"No box to pick in column {from_x}")
                return False

            self.from_x = from_x
            self.to_x = to_x
            self.box = stacks[from_x].pop()  # Remove top box from source stack
            self.box.landed = False  # Mark box as "in the air"
            self.state = "moving_to_pick"  # Begin movement sequence
            # Calculate height just above top box in from_x stack (or ground if empty)
            self.target_y = self._get_stack_top_y(from_x) - BOX_HEIGHT - 20

            print(f"Robot started moving from {from_x} to {to_x}")
            return True
        return False

    # Helper: get the Y coordinate of the top of the stack at position x
    def _get_stack_top_y(self, x):
        return GROUND_Y - len(stacks[x]) * BOX_HEIGHT

    # Update robot arm position and state machine every frame
    def update(self):
        if self.state == "idle":
            return  # Nothing to do if idle

        # Move horizontally above the stack to pick box
        if self.state == "moving_to_pick":
            target_x = self.from_x
            # Move robot_x toward target_x by self.speed pixels
            if abs(self.robot_x - target_x) > self.speed:
                self.robot_x += self.speed if self.robot_x < target_x else -self.speed
            else:
                self.robot_x = target_x
                self.state = "picking"  # Reached above box, start lowering
            return

        # Lower the arm vertically to reach the box
        if self.state == "picking":
            if self.robot_y < self.target_y:
                self.robot_y += self.speed
            else:
                self.robot_y = self.target_y
                self.state = "lifting"  # Picked box, start lifting up
            return

        # Lift the arm up with the box
        if self.state == "lifting":
            if self.robot_y > 100:
                self.robot_y -= self.speed
                self.box.y = self.robot_y + 20  # Move box along with arm vertically
                self.box.x = self.robot_x
            else:
                self.robot_y = 100
                self.state = "moving_to_place"  # Move horizontally to place position
            return

        # Move horizontally above the target stack to place box
        if self.state == "moving_to_place":
            target_x = self.to_x
            if abs(self.robot_x - target_x) > self.speed:
                direction = self.speed if self.robot_x < target_x else -self.speed
                self.robot_x += direction
                self.box.x = self.robot_x
                self.box.y = self.robot_y + 20
            else:
                self.robot_x = target_x
                # Calculate target Y to lower arm above top of target stack
                self.state = "lowering"
                self.target_y = self._get_stack_top_y(self.to_x) - BOX_HEIGHT - 20
            return

        # Lower arm vertically to place box down
        if self.state == "lowering":
            if self.robot_y < self.target_y:
                self.robot_y += self.speed
                self.box.y = self.robot_y + 20
                self.box.x = self.robot_x
            else:
                self.robot_y = self.target_y
                self.state = "releasing"  # Ready to release box
            return

        # Release the box (drop it, add to falling boxes list) and reset robot state
        if self.state == "releasing":
            self.box.vy = 0  # Reset vertical velocity for falling
            falling_boxes.append(self.box)  # Add to falling boxes list
            self.box = None
            self.state = "vertical_idle"  # Robot is free again
            self.from_x = None
            self.to_x = None
        
        if self.state == "vertical_idle":
            if self.robot_y > 100:
                self.robot_y -= self.speed
            else:
                self.robot_y = 100
                self.state = "idle"  # Robot is back to idle state after releasing box
            return
        # Reset robot arm to idle state if it has reached the ground level


    # Draw the robot arm on the screen
    def draw(self, screen):
        # Base of robot arm
        base_rect = pygame.Rect(self.robot_x - 30, 50, 60, 20)
        pygame.draw.rect(screen, (100, 100, 100), base_rect, border_radius=5)

        # Vertical arm (from base to gripper)
        arm_rect = pygame.Rect(self.robot_x - 10, 70, 20, self.robot_y - 70)
        pygame.draw.rect(screen, (70, 70, 70), arm_rect, border_radius=5)

        # Gripper part that holds the box
        grip_y = self.robot_y
        grip_width = 60
        grip_height = 15
        grip_rect = pygame.Rect(self.robot_x - grip_width // 2, grip_y, grip_width, grip_height)
        pygame.draw.rect(screen, (50, 50, 50), grip_rect, border_radius=5)

        # Two fingers of the gripper on left and right side
        finger_width = 10
        finger_height = grip_height
        left_finger = pygame.Rect(self.robot_x - grip_width // 2, grip_y, finger_width, finger_height)
        right_finger = pygame.Rect(self.robot_x + grip_width // 2 - finger_width, grip_y, finger_width, finger_height)
        pygame.draw.rect(screen, (80, 80, 80), left_finger, border_radius=3)
        pygame.draw.rect(screen, (80, 80, 80), right_finger, border_radius=3)

        # If robot is holding a box, draw it at the gripper position
        if self.box:
            self.box.draw(screen)

# Function to spawn initial boxes at the first stack at start of simulation
def spawn_initial_boxes():
    letters = ['A', 'B', 'C']  # Letters to put on boxes
    random.shuffle(letters)  # Shuffle order to randomize
    used_colors = []  # Track colors already used to avoid repetition

    for letter in letters:
        # Pick a color that hasn't been used yet
        available_colors = [c for c in COLOR_LIST if c not in used_colors]
        color = random.choice(available_colors)
        used_colors.append(color)

        # Create box at stack 1 position, letter and color assigned
        box = Box(STACK_X_POSITIONS[0], letter=letter, color=color)

        # Add box to falling boxes list to simulate falling at start
        falling_boxes.append(box)

# Draw text labels under each stack to identify them
def draw_stack_labels():
    labels = ["Stack 1", "Stack 2", "Stack 3"]
    for x, label in zip(STACK_X_POSITIONS, labels):
        text = label_font.render(label, True, TEXT_COLOR)
        # Position label centered below each stack column
        text_rect = text.get_rect(center=(x, GROUND_Y + 30))
        screen.blit(text, text_rect)

stack_name_to_pos = {
    'Stack 1': STACK_X_POSITIONS[0],
    'Stack 2': STACK_X_POSITIONS[1],
    'Stack 3': STACK_X_POSITIONS[2],
}


def get_status(stacks):
    status = {}
    for stack_name, x_pos in stack_name_to_pos.items():
        boxes = stacks.get(x_pos, [])  # Note: stacks keys are x positions, not 'stack0' strings
        box_letters = [box.letter for box in boxes]  # Extract letters from Box objects
        status[stack_name] = {
            'boxes from bottom to top': box_letters,
        }
    return status


def parse_move_command(command_str):
    """
    Parses command like: move(Stack 1, Stack 2)
    Returns tuple (from_x, to_x) if valid, else None
    """
    pattern = r'move\(\s*stack\s*(\d)\s*,\s*stack\s*(\d)\s*\)'
    match = re.match(pattern, command_str.strip().lower())
    if match:
        from_idx, to_idx = match.groups()
        from_stack = f"Stack {from_idx}"
        to_stack = f"Stack {to_idx}"
        if from_stack in stack_name_to_pos and to_stack in stack_name_to_pos:
            return stack_name_to_pos[from_stack], stack_name_to_pos[to_stack]
    return None


# Socket listener function to receive key commands
def socket_listener():
    HOST = '127.0.0.1'
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Socket server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    command_str = data.decode('utf-8').strip()
                    print(f"Received command via socket: {command_str}")
                    
                    if command_str == "get_status":
                        # Get current stack stats as string
                        stats = get_status(stacks)  # assuming `stacks` is your data structure
                        stats_str = str(stats)
                        conn.sendall(stats_str.encode('utf-8'))
                        print("Sent stack status to client.")
                        continue


                    elif command_str.lower().startswith("move"):
                        move_params = parse_move_command(command_str)
                        if move_params and robot.state == "idle":
                            from_x, to_x = move_params
                            started = robot.start_move(from_x, to_x)
                            # Send only "True" or "False"
                            conn.sendall(str(started).encode('utf-8'))
                        elif not move_params:
                            print("Invalid move command format")
                            conn.sendall(b"False")
                        else:
                            print("Robot busy, ignoring command.")
                            conn.sendall(b"False")


# Main program

spawn_initial_boxes()
robot = RobotArm()

# Start socket listener in a separate daemon thread
listener_thread = threading.Thread(target=socket_listener, daemon=True)
listener_thread.start()


running = True  # Main loop condition
while running:
    screen.fill(WHITE)  # Clear screen each frame

    # Event processing loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Window close button clicked
            running = False

        elif event.type == pygame.KEYDOWN:
            # If robot is busy moving, ignore new commands
            if robot.state != "idle":
                continue

            # Map keyboard keys to robot arm moves between stacks
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

    # Update robot arm position and state machine
    robot.update()

    # Update all falling boxes (apply gravity, check for landing) and draw them
    for box in falling_boxes[:]:
        box.update()
        box.draw(screen)
        # Remove boxes from falling list once landed (they get added to stacks automatically)
        if box.landed:
            falling_boxes.remove(box)

    # Draw all stacked boxes (boxes already landed on stacks)
    for x in stacks:
        for box in stacks[x]:
            box.draw(screen)

    # Draw the robot arm
    robot.draw(screen)

    # Draw labels for the stacks below
    draw_stack_labels()

    # Update the display with everything drawn this frame
    pygame.display.flip()
    clock.tick(FPS)  # Maintain fixed FPS to keep animation smooth

pygame.quit()  # Clean up pygame resources when loop ends
sys.exit()
