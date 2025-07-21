import pygame
import os
import random
import threading
from box import Box
from robot_arm import RobotArm
from api import command_queue, status_queue, reply_queue, run_flask
import simulation_settings as settings

# Main function to run the Pygame loop
def pygame_mainloop():
    
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
        status['robot'] = robot.state
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

    def process_status_queries():
        while not status_queue.empty():
            status_cmd = status_queue.get()
            if status_cmd[0] == 'get_status':
                current_status = get_current_status(stacks)
                reply_queue.put(current_status)
            elif status_cmd[0] == 'check_free_stack':
                free_stack = robot.find_free_stack()
                if free_stack is not None:
                    reply_queue.put(f"Free stack available at stack {free_stack}.")
                else:
                    reply_queue.put("No free stack available.")

    def process_commands():
        while not command_queue.empty():
            cmd = command_queue.get()
            if cmd[0] == 'pick_up':
                robot.pick_up(cmd[1])
            elif cmd[0] == 'unstack':
                robot.unstack(cmd[1], cmd[2])
            elif cmd[0] == 'put_down':
                robot.put_down(cmd[1])
            elif cmd[0] == 'stack':
                robot.stack(cmd[1], cmd[2])

    def handle_pygame_events():
        nonlocal running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if robot.state != "idle" and robot.state != "holding":
                    continue
                # Pickup block with letters: 'A', 'B', 'C', 'D', ...
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

    def update_and_draw():
        # Update robot arm
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

    robot = RobotArm(settings.STACK_X_POSITIONS, stacks, falling_boxes)

    # Main loop
    running = True
    while running:
        screen.fill(settings.WHITE)
  
        # Process API requests and pygame events
        process_status_queries()
        process_commands()
        handle_pygame_events()

        # Update and draw all game elements
        update_and_draw()

        # Update the display
        pygame.display.flip()
        clock.tick(settings.FPS)

    pygame.quit()
    os._exit(0)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run pygame on the main thread (required for macOS)
    pygame_mainloop()

# Example usage of the REST API:               
# r = requests.post(f"http://localhost:5001/unstack", json={"block1": 'A', "block2": 'B'}, timeout=2)
# to test this with curl:
# curl -X POST -H "Content-Type: application/json" -d '{"block1": "A", "block2": "B"}' http://localhost:5001/unstack
