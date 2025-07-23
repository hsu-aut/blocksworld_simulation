import pygame
import os
import random
from .box import Box
from .robot import Robot
from blocksworld_simulation.api.api import api_in_queue, api_out_queue
from . import settings
from .robot import RobotState

# Main function to run the Pygame loop
def start_pygame_mainloop():
    
    def spawn_initial_boxes():
        letters = settings.INITIAL_BOX_LETTERS.copy()
        random.shuffle(letters)
        # Pick distinct colors for boxes without repetition
        used_colors = []
        for letter in letters:
            available_colors = [c for c in settings.COLOR_LIST if c not in used_colors]
            color = random.choice(available_colors)
            used_colors.append(color)
            x_pos = random.choice(settings.STACK_X_POSITIONS)
            box = Box(x_pos, letter=letter, color=color, stacks=stacks)
            falling_boxes.append(box)

    def get_current_status(stacks):
        status = {}
        status['robot'] = robot.state.value
        status['holding'] = robot.box.letter if robot.box else None
        status['total number of stacks'] = len(settings.STACK_X_POSITIONS)
        for stack_name, x_pos in stack_name_to_pos.items():
            boxes = stacks.get(x_pos, [])  # Note: stacks keys are x positions, not 'stack0' strings
            box_letters = [box.letter for box in boxes]  # Extract letters from Box objects
            status[stack_name] = {
                'boxes from bottom to top': box_letters,
            }
        return status

    def draw_stack_labels():
        labels = list(stack_name_to_pos.keys())
        for x, label in zip(settings.STACK_X_POSITIONS, labels):
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

    # Initialize Pygame
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.CAPTION)

    # State
    stacks = {x: [] for x in settings.STACK_X_POSITIONS}
    falling_boxes = []

    # Init clock
    clock = pygame.time.Clock()

    # Init font
    font = pygame.font.SysFont(settings.MAIN_FONT_NAME, settings.MAIN_FONT_SIZE, bold=True)
    label_font = pygame.font.SysFont(settings.MAIN_FONT_NAME, settings.LABEL_FONT_SIZE, bold=False)

    # Map stack names to their x positions
    stack_name_to_pos = {
        f'stack {i+1}': pos for i, pos in enumerate(settings.STACK_X_POSITIONS)
    }

    # Spawn initial boxes
    spawn_initial_boxes()

    robot = Robot(settings.STACK_X_POSITIONS, stacks, falling_boxes)

    # Main loop
    running = True
    while running:
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
    os._exit(0)