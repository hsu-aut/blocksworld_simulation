import pygame
import os
import random
from .box import Box
from .robot import Robot
from blocksworld_simulation.api.api import api_in_queue, api_out_queue
from . import settings
from .robot import RobotState

stop_simulation = False
stack_x_positions = []

# Main function to run the Pygame loop
def start_pygame_mainloop(initial_setup=None, num_boxes=None):
    
    # calculate stack positions based on the number of stacks
    def calculate_stack_positions():
        stack_number = len(initial_setup) if initial_setup else random.randint(2, 5)
        global stack_x_positions 
        stack_x_positions = [settings.STACK_X_POSITION_LEFT + i * (settings.STACK_X_POSITION_RIGHT - settings.STACK_X_POSITION_LEFT) // (stack_number - 1)
                    for i in range(stack_number)]
    
    def spawn_initial_boxes():
        
        # Use provided stack setup if available
        if initial_setup:
            for idx, letters in initial_setup.items():
                x_pos = stack_x_positions[int(idx)]
                for letter in letters:
                    color = random.choice(settings.COLOR_LIST)
                    box = Box(x_pos, letter=letter, color=color, stacks=stacks)
                    falling_boxes.append(box)
            return
        
        # otherwise spawn random boxes using number provided or default
        count = num_boxes if num_boxes is not None else random.randint(2, 5)
        letters = [settings.LETTERS[i % len(settings.LETTERS)] for i in range(count)]

        random.shuffle(letters)
        # Pick distinct colors for boxes without repetition
        used_colors = []
        for letter in letters:
            available_colors = [c for c in settings.COLOR_LIST if c not in used_colors]
            color = random.choice(available_colors)
            used_colors.append(color)
            x_pos = random.choice(stack_x_positions)
            box = Box(x_pos, letter=letter, color=color, stacks=stacks)
            falling_boxes.append(box)

    def get_current_status(stacks):
        status = {}
        status['robot'] = robot.state.value
        status['holding'] = robot.box.letter if robot.box else None
        status['total number of stacks'] = len(stack_x_positions)
        for stack_name, x_pos in stack_name_to_pos.items():
            boxes = stacks.get(x_pos, [])  # Note: stacks keys are x positions, not 'stack0' strings
            box_letters = [box.letter for box in boxes]  # Extract letters from Box objects
            status[stack_name] = {
                'boxes from bottom to top': box_letters,
            }
        return status

    def draw_stack_labels():
        labels = list(stack_name_to_pos.keys())
        for x, label in zip(stack_x_positions, labels):
            text = label_font.render(label, True, settings.TEXT_COLOR)
            text_rect = text.get_rect(center=(x, settings.GROUND_Y+20))
            screen.blit(text, text_rect)

    def process_api_queues():
        if not api_in_queue.empty():
            # get the item in the queue
            api_cmd = api_in_queue.get()
            if api_cmd[0] == 'get_status':
                current_status = get_current_status(stacks)
                api_out_queue.put(current_status)
            elif api_cmd[0] == 'check_free_stack':
                free_stack = robot.find_free_stack()
                if free_stack is not None:
                    api_out_queue.put(f"Free stack available at stack {free_stack}.")
                else:
                    api_out_queue.put("No free stack available.")
            # when command is for robot, pass api_out_queue to robot
            # in order to get the result back
            elif api_cmd[0] == 'pick_up':
                robot.pick_up(api_out_queue, api_cmd[1])
            elif api_cmd[0] == 'unstack':
                robot.unstack(api_out_queue, api_cmd[1], api_cmd[2])
            elif api_cmd[0] == 'put_down':
                robot.put_down(api_out_queue, api_cmd[1])
            elif api_cmd[0] == 'stack':
                robot.stack(api_out_queue, api_cmd[1], api_cmd[2])

    def handle_pygame_events():
        nonlocal running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if robot.state != RobotState.IDLE and robot.state != RobotState.HOLDING:
                    continue
                # Pickup block with letters: 'A', 'B', 'C', 'D', ...
                if robot.state == RobotState.IDLE and robot.box is None:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        robot.pickup_by_letter(letter)
                elif robot.state == RobotState.HOLDING and robot.box is not None:
                    if pygame.K_a <= event.key <= pygame.K_z:
                        letter = chr(event.key).upper()
                        robot.put_down_on_letter(letter)
                    elif event.key == pygame.K_SPACE:
                        robot.put_down_on_ground()

    def update_and_draw():
        # Update robot
        robot.update()

        # Update falling boxes
        for box in falling_boxes[:]:
            box.update()
            box.draw(screen, font)
            if box.landed:
                falling_boxes.remove(box)

        # Draw stacked boxes
        for x in stacks:
            for box in stacks[x]:
                box.draw(screen, font)

        # Draw robot
        robot.draw(screen)

        # Draw stack labels below columns
        draw_stack_labels()

    global stop_simulation
    stop_simulation = False

    # Initialize Pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.CAPTION)

    # State
    calculate_stack_positions() 
    stacks = {x: [] for x in stack_x_positions}
    falling_boxes = []

    # Init clock
    clock = pygame.time.Clock()

    # Init font
    font = pygame.font.SysFont(settings.MAIN_FONT_NAME, settings.MAIN_FONT_SIZE, bold=True)
    label_font = pygame.font.SysFont(settings.MAIN_FONT_NAME, settings.LABEL_FONT_SIZE, bold=False)

    # Map stack names to their x positions
    stack_name_to_pos = {
        f'stack {i+1}': pos for i, pos in enumerate(stack_x_positions)
    }

    # Spawn initial boxes
    spawn_initial_boxes()

    robot = Robot(stack_x_positions, stacks, falling_boxes)

    # Main loop
    running = True
    while running and not stop_simulation:
        screen.fill(settings.WHITE)

        # Process API requests and pygame events
        process_api_queues()
        handle_pygame_events()

        # Update and draw all game elements
        update_and_draw()

        # Update the display
        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()
    # os._exit(0)