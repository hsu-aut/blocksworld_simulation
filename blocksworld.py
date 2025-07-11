import pygame
import os
import random
from flask import Flask, request, jsonify
import threading
import queue

app=Flask(__name__)
command_queue = queue.Queue()
status_queue = queue.Queue()
reply_queue = queue.Queue()


# Defines the Flask routes for the robot actions and the status requests
@app.route('/pick_up', methods=['POST'])
def pick_up():
    data = request.get_json()
    block = data.get('block')
    command_queue.put(('pick_up', block))
    return jsonify({"result": f"Command pick_up {block} queued."})

@app.route('/put_down', methods=['POST'])
def put_down():
    data = request.get_json()
    block = data.get('block')
    command_queue.put(('put_down', block))
    return jsonify({"result": f"Command put_down {block} queued."})

@app.route('/stack', methods=['POST'])
def stack():
    data = request.get_json()
    block1 = data.get('block1')
    block2 = data.get('block2')
    command_queue.put(('stack', block1, block2))
    return jsonify({"result": f"Command stack {block1} on {block2} queued."})

@app.route('/get_status', methods=['POST'])
def get_status():
    #Get the status of the stacks
    status_queue.put(('get_status',))
    try:
        status_received = reply_queue.get(timeout=2) #wait for 2s for a reply
        return jsonify({"result": f"{status_received}"})
    except queue.Empty:
        return jsonify({"result": "No status available."})


    
# Main function to run the Pygame loop
def pygame_mainloop():
    pygame.init()

    # Screen setup
    WIDTH, HEIGHT = 850, 500
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
    STACK_X_POSITIONS = [200, 350, 500, 650]  # X positions for the stacks
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
            shadow.move_ip(3, 3)
            pygame.draw.rect(screen, SHADOW_COLOR, shadow, border_radius=12)

            # Box
            pygame.draw.rect(screen, self.color, rect, border_radius=12)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 2, border_radius=12)

            # Letter
            text = font.render(self.letter, True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    # Find a box by its letter in the stacks
    def find_box_by_letter(letter):
        for stack_x in stacks:
            stack = stacks[stack_x]
            if stack and stack[-1].letter.upper() == letter.upper():
                return stack_x
        return None

    # Find a free stack (one that has no boxes)
    def find_free_stack():
        for x in stacks:
            if not stacks[x]:
                return x
        return None

    class RobotArm:
        def __init__(self):
            self.robot_x = STACK_X_POSITIONS[0]
            self.robot_y = 100  # initial height
            self.speed = 8
            self.state = "idle"  # idle, moving_to_pick, picking, lifting, moving_to_place, lowering, releasing, holding
            self.box = None
            self.from_x = None
            self.to_x = None
            self.target_y = None


        def _get_stack_top_y(self, x):
            return GROUND_Y - len(stacks[x]) * BOX_HEIGHT
        
        #Pickup a box with a specific letter
        def pickup_by_letter(self, letter):
            if self.state == "idle" and self.box is None:
                stack_x = find_box_by_letter(letter)
                if stack_x is not None:
                    return self.pickup(stack_x)
                print(f" Block {letter} is not available!")
                return False
            print("Cannot pickup.")
            return False
        
        # Put down a box on a Box with a specific letter
        def put_down_on_letter(self, target_letter):
            if self.state == "holding" and self.box is not None:
                stack_x = find_box_by_letter(target_letter)
                if stack_x is not None:
                    return self.put_down(stack_x)
                else:
                    print(f"Block {target_letter} is not free!")
                    return False
            print("No block is held!")
            return False
        
        # Put down a box on the ground
        def put_down_on_ground(self):
            if self.state == "holding" and self.box is not None:
                stack_x = find_free_stack()
                if stack_x is not None:
                    return self.put_down(stack_x)
                else:
                    print("No free Stack!")
                    return False
            print("No block is held!")
            return False

        # Pickup a box from a specific stack
        def pickup(self, from_x):
            if self.state == "idle" and self.box is None and stacks[from_x]:
                self.from_x = from_x
                self.to_x = from_x
                self.box = stacks[from_x].pop()
                self.box.landed = False
                self.state = "moving_to_pick"
                self.target_y = self._get_stack_top_y(from_x) - BOX_HEIGHT - 20
                print(f"Picked up box from {from_x}")
                return True
            print("Cannot pickup.")
            return False

        # Put down a box to a specific stack
        def put_down(self, to_x):
            if self.state == "holding" and self.box is not None:
                self.from_x = None
                self.to_x = to_x
                self.state = "moving_to_place"
                self.target_y = self._get_stack_top_y(to_x) - BOX_HEIGHT - 20
                print(f"Putting down box to {to_x}")
                return True
            print("Cannot put down.")
            return False

        # Updates the robot arm's state and position (like state machine)
        def update(self):
            if self.state == "idle":
                return
            
            if self.state == "holding":
                if self.robot_y > 100:
                    self.robot_y -= self.speed
                    self.box.y = self.robot_y + 20
                    self.box.x = self.robot_x
                else:
                    self.robot_y = 100
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
                    self.state = "holding"
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
                if self.box != None:
                    self.box.vy = 0
                    falling_boxes.append(self.box)
                    self.box = None
                    self.from_x = None
                    self.to_x = None

                if self.robot_y > 100:
                    self.robot_y -= self.speed
                else:
                    self.robot_y = 100
                    self.state = "idle"
                

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
        letters = ['A', 'B', 'C', 'D']
        random.shuffle(letters)
        # Pick distinct colors for boxes without repetition
        used_colors = []
        for letter in letters:
            available_colors = [c for c in COLOR_LIST if c not in used_colors]
            color = random.choice(available_colors)
            used_colors.append(color)
            box = Box(STACK_X_POSITIONS[0], letter=letter, color=color)
            falling_boxes.append(box)

    stack_name_to_pos = {
        'Stack 1': STACK_X_POSITIONS[0],
        'Stack 2': STACK_X_POSITIONS[1],
        'Stack 3': STACK_X_POSITIONS[2],
    }

    def get_current_status(stacks):
        status = {}
        status['robot'] = robot.state
        status['holding'] = robot.box.letter if robot.box else None
        for stack_name, x_pos in stack_name_to_pos.items():
            boxes = stacks.get(x_pos, [])  # Note: stacks keys are x positions, not 'stack0' strings
            box_letters = [box.letter for box in boxes]  # Extract letters from Box objects
            status[stack_name] = {
                'boxes from bottom to top': box_letters,
            }
        return status

    def draw_stack_labels():
        labels = ["Stack 1", "Stack 2", "Stack 3", "Stack 4"]
        for x, label in zip(STACK_X_POSITIONS, labels):
            text = label_font.render(label, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x, GROUND_Y))  # Below ground line
            screen.blit(text, text_rect)

    # Spawn initial boxes
    spawn_initial_boxes()

    robot = RobotArm()

    running = True
    while running:
        screen.fill(WHITE)

  
        # Processing Status Queries
        while not status_queue.empty():
            status_cmd = status_queue.get()
            if status_cmd[0] == 'get_status':
                current_status = get_current_status(stacks)
                reply_queue.put(current_status)
               

        # Processing Commands
        while not command_queue.empty():
            cmd = command_queue.get()
            if cmd[0] == 'pick_up':
                robot.pickup_by_letter(cmd[1])
            elif cmd[0] == 'unstack':
                robot.pickup_by_letter(cmd[1])
            elif cmd[0] == 'put_down':
                robot.put_down_on_ground()
            elif cmd[0] == 'stack':
                robot.put_down_on_letter(cmd[2])
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if robot.state != "idle" and robot.state != "holding":
                    continue
                # Pickup block with letters: ‘A’, ‘B’, ‘C’, ‘D’, ...
                if robot.state == "idle" and robot.box is None:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        robot.pickup_by_letter(letter)
                elif robot.state == "holding" and robot.box is not None:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        robot.put_down_on_letter(letter)
                    elif event.key == pygame.K_SPACE:
                        robot.put_down_on_ground()

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
    os._exit(0)

# Run the Flask app and Pygame loop in separate threads
if __name__ == "__main__":
    t = threading.Thread(target=pygame_mainloop)
    t.daemon = True
    t.start()
    app.run(port=5001)
