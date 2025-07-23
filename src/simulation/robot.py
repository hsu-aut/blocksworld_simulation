from enum import Enum
from . import settings as settings
from .robot_drawer import RobotDrawer
import queue

# define robot states as enum
class RobotState(Enum):
        IDLE = "idle"
        MOVING_TO_PICK = "moving_to_pick"
        PICKING = "picking"
        LIFTING = "lifting"
        HOLDING = "holding"
        MOVING_TO_PLACE = "moving_to_place"
        LOWERING = "lowering"
        RELEASING = "releasing"

class Robot:

    def __init__(self, stack_positions=None, stacks=None, falling_boxes=None):
        self.stack_positions = stack_positions or settings.STACK_X_POSITIONS
        self.robot_x = self.stack_positions[0]
        self.robot_y = settings.ROBOT_BASE_Y
        self.speed = settings.ROBOT_SPEED
        self.state = RobotState.IDLE
        self.box = None
        self.from_x = None
        self.to_x = None
        self.target_y = None
        self.stacks = stacks or {}
        self.falling_boxes = falling_boxes or []
        # drawer for the robot
        self.drawer = RobotDrawer()
        # queues for API commands
        self.pick_up_queue = queue.Queue()
        self.unstack_queue = queue.Queue()
        self.stack_queue = queue.Queue()
        self.put_down_queue = queue.Queue()

    def get_stack_top_y(self, x):
        if not self.stacks:
            return settings.GROUND_Y
        ground_y = settings.GROUND_Y
        box_height = settings.BOX_HEIGHT
        return ground_y - len(self.stacks[x]) * box_height

    def find_box_by_letter(self, letter):
        for stack_x in self.stacks:
            stack = self.stacks[stack_x]
            if stack and stack[-1].letter.upper() == letter.upper():
                return stack_x
        return None

    def find_free_stack(self):
        for x in self.stacks:
            if not self.stacks[x]:
                return x
        return None

    def pick_up(self, api_out_queue, letter):
        """ API-compatible pick up method """
        if self.state == RobotState.IDLE and self.box is None:
            stack_x = self.find_box_by_letter(letter)
            if stack_x is not None and len(self.stacks[stack_x]) <= 1:
                # init pick up and put item on pick up queue
                self.pick_up_queue.put((letter, api_out_queue))
                return self.pickup_stack(stack_x)
            api_out_queue.put(f" Block {letter} is not available or is not on the ground!")
            return False
        api_out_queue.put("Cannot pickup.")
        return False

    def unstack(self, api_out_queue, letter, lower_letter):
        """ API-compatible unstack method """
        if self.state == RobotState.IDLE and self.box is None:
            stack_x = self.find_box_by_letter(letter)
            if (stack_x is not None and len(self.stacks[stack_x]) >= 2 
                and self.stacks[stack_x][-2].letter.upper() == lower_letter.upper()):
                # init unstack and put item on unstack queue
                self.unstack_queue.put((letter, lower_letter, api_out_queue))
                return self.pickup_stack(stack_x)
            api_out_queue.put(f" Block {letter} is not available or wrong unstack letter {lower_letter}!")
            return False
        api_out_queue.put("Cannot pickup.")
        return False

    def stack(self, api_out_queue, letter, target_letter):
        """ API-compatible stack method """
        if self.state == RobotState.HOLDING:
            if self.box.letter.upper() == letter.upper():
                stack_x = self.find_box_by_letter(target_letter)
                if stack_x is not None:
                    # init stack and put item on stack queue
                    self.stack_queue.put((letter, target_letter, api_out_queue))
                    return self.put_down_stack(stack_x)
                else:
                    api_out_queue.put(f"Block {target_letter} is not free!")
                    return False
            else:
                api_out_queue.put(f"Block {letter.upper()} is not held!")
                return False
        api_out_queue.put("No block is held!")
        return False

    def put_down(self, api_out_queue, letter):
        """ API-compatible put down method """
        if self.state == RobotState.HOLDING:
            if self.box.letter.upper() == letter.upper():
                stack_x = self.find_free_stack()
                if stack_x is not None:
                    # init put down and put item on put down queue
                    self.put_down_queue.put((letter, api_out_queue))
                    return self.put_down_stack(stack_x)
                else:
                    api_out_queue.put("No free stack!")
                    return False
            else:
                api_out_queue.put(f"Block {letter.upper()} is not held!")
                return False
        api_out_queue.put("No block is held!")
        return False

    def pickup_by_letter(self, letter):
        """ Keyboard-input compatible pickup method """
        if self.state == RobotState.IDLE and self.box is None:
            stack_x = self.find_box_by_letter(letter)
            if stack_x is not None:
                return self.pickup_stack(stack_x)
            print(f" Block {letter} is not available!")
            return False
        print("Cannot pickup.")
        return False

    def put_down_on_letter(self, target_letter):
        """ Keyboard-input compatible put down method """
        if self.state == RobotState.HOLDING and self.box is not None:
            stack_x = self.find_box_by_letter(target_letter)
            if stack_x is not None:
                return self.put_down_stack(stack_x)
            else:
                print(f"Block {target_letter} is not free!")
                return False
        print("No block is held!")
        return False

    def put_down_on_ground(self):
        """ Keyboard-input compatible put down method """
        if self.state == RobotState.HOLDING and self.box is not None:
            stack_x = self.find_free_stack()
            if stack_x is not None:
                return self.put_down_stack(stack_x)
            else:
                print("No free stack!")
                return False
        print("No block is held!")
        return False

    def pickup_stack(self, from_x):
        """ Actual pickup method, triggered by API or keyboard input """
        if self.state == RobotState.IDLE and self.box is None and self.stacks[from_x]:
            self.from_x = from_x
            self.to_x = from_x
            self.box = self.stacks[from_x].pop()
            self.box.landed = False
            self.state = RobotState.MOVING_TO_PICK
            self.target_y = self.get_stack_top_y(from_x) - settings.BOX_HEIGHT - 20
            print(f"Picked up box from {from_x}")
            return True
        print("Cannot pickup.")
        return False

    def put_down_stack(self, to_x):
        """ Actual put down method, triggered by API or keyboard input """
        if self.state == RobotState.HOLDING and self.box is not None:
            self.from_x = None
            self.to_x = to_x
            self.state = RobotState.MOVING_TO_PLACE
            self.target_y = self.get_stack_top_y(to_x) - settings.BOX_HEIGHT - 20
            print(f"Putting down box to {to_x}")
            return True
        print("Cannot put down.")
        return False

    def update(self):
        if self.state == RobotState.IDLE:
            return

        if self.state == RobotState.HOLDING:
            if self.robot_y > settings.ROBOT_BASE_Y:
                self.robot_y -= self.speed
                if self.box:
                    self.box.y = self.robot_y + 20
                    self.box.x = self.robot_x
            else:
                self.robot_y = settings.ROBOT_BASE_Y
            return

        if self.state == RobotState.MOVING_TO_PICK:
            target_x = self.from_x
            if abs(self.robot_x - target_x) > self.speed:
                self.robot_x += self.speed if self.robot_x < target_x else - self.speed
            else:
                self.robot_x = target_x
                self.state = RobotState.PICKING
            return

        if self.state == RobotState.PICKING:
            if self.robot_y < self.target_y:
                self.robot_y += self.speed
            else:
                self.robot_y = self.target_y
                self.state = RobotState.LIFTING
            return

        if self.state == RobotState.LIFTING:
            if self.robot_y > settings.ROBOT_BASE_Y:
                self.robot_y -= self.speed
                if self.box:
                    self.box.y = self.robot_y + 20
                    self.box.x = self.robot_x
            else:
                self.robot_y = settings.ROBOT_BASE_Y
                self.state = RobotState.HOLDING
                # if pick up queue is not empty
                if not self.pick_up_queue.empty():
                    item = self.pick_up_queue.get()
                    letter = item[0]
                    api_out_queue = item[1]
                    api_out_queue.put(f"Picked up block {letter}.")
                # if unstack queue is not empty
                if not self.unstack_queue.empty():
                    item = self.unstack_queue.get()
                    letter = item[0]
                    lower_letter = item[1]
                    api_out_queue = item[2]
                    api_out_queue.put(f"Unstacked block {letter} from {lower_letter}.")
            return

        if self.state == RobotState.MOVING_TO_PLACE:
            target_x = self.to_x
            if abs(self.robot_x - target_x) > self.speed:
                direction = self.speed if self.robot_x < target_x else -self.speed
                self.robot_x += direction
                if self.box:
                    self.box.x = self.robot_x
                    self.box.y = self.robot_y + 20
            else:
                self.robot_x = target_x
                self.state = RobotState.LOWERING
                self.target_y = self.get_stack_top_y(self.to_x) - settings.BOX_HEIGHT - 20
            return

        if self.state == RobotState.LOWERING:
            if self.robot_y < self.target_y:
                self.robot_y += self.speed
                if self.box:
                    self.box.y = self.robot_y + 20
                    self.box.x = self.robot_x
            else:
                self.robot_y = self.target_y
                self.state = RobotState.RELEASING
            return

        if self.state == RobotState.RELEASING:
            if self.box is not None:
                self.box.vy = 0
                self.falling_boxes.append(self.box)
                self.box = None
                self.from_x = None
                self.to_x = None
            if self.robot_y > settings.ROBOT_BASE_Y:
                self.robot_y -= self.speed
            else:
                self.robot_y = settings.ROBOT_BASE_Y
                self.state = RobotState.IDLE
                # if put down queue is not empty
                if not self.put_down_queue.empty():
                    item = self.put_down_queue.get()
                    letter = item[0]
                    api_out_queue = item[1]
                    api_out_queue.put(f"Put down block {letter}.")
                # if stack queue is not empty
                if not self.stack_queue.empty():
                    item = self.stack_queue.get()
                    letter = item[0]
                    target_letter = item[1]
                    api_out_queue = item[2]
                    api_out_queue.put(f"Stacked block {letter} on {target_letter}.")
            return

    def draw(self, screen):
        self.drawer.draw(screen, self.robot_x, self.robot_y, self.box)