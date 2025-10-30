from queue import Queue
import pygame
import logging

from .user_input_handler import handle_user_inputs
from blocksworld_simulation.constraints.constraint_manager import constraint_manager
from blocksworld_simulation.scenarios.scenario_manager import scenario_manager
from .stack_creator import create_stacks
from .robot import Robot
from .simulation_actions import (
    PreStartAction, SimulationAction, QuitAction, 
    StartAction, StopAction, RobotAction, GetStatusAction, 
    GetRulesAction, GetScenarioAction, PlanAction
)
from .simulation_state import SimulationState
import copy


logger = logging.getLogger(__name__)

class BlocksWorldSimulation:
    """Main simulation class that manages the blocks world simulation"""
    
    def __init__(self, api_to_sim_queue: Queue, sim_to_api_queue: Queue, width: int = 1000, height: int = 600):
        """Initialize the simulation with given width and height"""
        # Initialize pygame
        pygame.init()
        self._width = width
        self._height = height
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Blocks World Simulation")
        # Initialize clock for frame rate control
        self._fps = 60
        self._clock = pygame.time.Clock()
        # Application state
        self._app_running = False
        # Application mode (Verification mode: execute list of actions to be validated without gui, reset simulation afterwards)
        self._verification_mode = False
        # Simulation state
        self._simulation_state: SimulationState = SimulationState(
            simulation_running=False,
            robot=None,
            stacks=[]
        )
        self._pre_verification_simulation_state: SimulationState = None
        # Queues for input/feedback to user and API
        self._local_reply_queue = Queue()
        self._api_to_sim_queue = api_to_sim_queue
        self._sim_to_api_queue = sim_to_api_queue
        # Queues etc. for executing plans
        self._current_execute_plan_action: PlanAction = None
        self._execute_plan_queue: Queue = Queue()
        self._execute_plan_reply_queue: Queue = Queue()

    def _init_simulation(self, stack_config = None):
        """Initialize the simulation (randomly or with given stacks)"""
        # Create random blocks or use provided stacks
        self._simulation_state.set_stacks(create_stacks(stack_config=stack_config))
        # initialize robot
        self._simulation_state.set_robot(Robot())
        # set simulation state to running
        self._simulation_state.set_simulation_running(True)
    
    def _handle_action(self, action: SimulationAction):
        """Handle the given action"""
        # If action is None or action is invalid, do nothing
        if action is None or not action.is_valid():
            return
        # If the action is a QuitAction, stop the application by setting _app_running flag
        if isinstance(action, QuitAction):
            self._app_running = False
            action.reply_success()
        # If the action is a StartAction, handle startup configuration
        elif isinstance(action, StartAction):
            self._init_simulation(action.get_stack_config())
            action.reply_success()
        # If the action is a PreStartAction, set constraint set and create the StartAction
        # do not reply success, this will be done by the StartAction
        elif isinstance(action, PreStartAction):
            constraint_manager.set_constraint_set(action.get_constraint_set())
            self._api_to_sim_queue.put(action.create_start_action())
        # If the action is a StopAction, stop the simulation by setting _simulation_running flag
        elif isinstance(action, StopAction):
            self._simulation_state.set_simulation_running(False)
            action.reply_success()
        elif isinstance(action, GetScenarioAction):
            action.set_result_data(scenario_manager.get_scenario_info(action.get_scenario_name()))
            action.reply_success()
        # If the action is a GetStatusAction, reply with the current status of the simulation
        elif isinstance(action, GetStatusAction):
            action.reply_success()
        # If the action is a GetRulesAction, reply with the current rules of the simulation
        elif isinstance(action, GetRulesAction):
            action.set_rules(constraint_manager.get_rules())
            action.reply_success()
        # If the action is a RobotAction, pass the action to the robot
        elif isinstance(action, RobotAction):
            self._simulation_state.get_robot().set_action(action)
        # If the action is a PlanAction, put actions in the execute plan processing queue
        elif isinstance(action, PlanAction):
            self._pre_verification_simulation_state = copy.deepcopy(self._simulation_state)
            self._current_execute_plan_action = action
            for sub_action in action.get_actions():
                self._execute_plan_queue.put(sub_action)
            self._verification_mode = action.is_in_verification_mode()
            self._simulation_state.get_robot().set_verification_mode(self._verification_mode)
        return

    def _log_local_reply_queue(self):
        """Log the contents of the local reply queue"""
        while not self._local_reply_queue.empty():
            success, message = self._local_reply_queue.get()
            logger.info(message) if success else logger.warning(message)

    def _handle_execute_plan_reply_queue(self):
        if not self._execute_plan_reply_queue.empty():
            success, message = self._execute_plan_reply_queue.get()
            # if success and last action, reply success via API, reset verification mode
            if success and self._execute_plan_queue.empty():
                self._current_execute_plan_action.reply_success()  
            # if not success, return error report via API, reset verification mode and clear queue
            elif not success:
                self._current_execute_plan_action.reply_plan_invalid(message)
            # in both cases, reset verification mode, queue and current action
            if (success and self._execute_plan_queue.empty()) or not success:
                # reset simulation state, if previously in verification mode
                if self._verification_mode:
                    self._simulation_state = self._pre_verification_simulation_state
                self._simulation_state.get_robot().set_verification_mode(False)
                self._verification_mode = False
                self._execute_plan_queue = Queue()

    def _draw(self):
        """Draw the simulation"""
        self._screen.fill((255, 255, 255))
        # if simulation is stopped, draw a message
        if not self._simulation_state.get_simulation_running():
            text = "Press <SPACE> to start randomly or use API to configure initial state"
            rendered_text = pygame.font.Font(None, 36).render(text, True, (0, 0, 0))
            text_rect = rendered_text.get_rect(center=(self._screen.get_size()[0] // 2, self._screen.get_size()[1] // 2))
            self._screen.blit(rendered_text, text_rect)
        # else, draw all components (stacks draw blocks in stack, robot draws held block)
        else:
            for stack in self._simulation_state.get_stacks():
                stack.draw(self._screen)
            self._simulation_state.get_robot().draw(self._screen)
        # update the display
        pygame.display.flip()

    def run(self):
        """Main application loop"""
        self._app_running = True
        while self._app_running:
            # check user inputs
            input_action = handle_user_inputs(self._simulation_state)
            input_action.set_reply_queue(self._local_reply_queue) if input_action else None
            # check for API inputs, overwriting user input 
            if not self._api_to_sim_queue.empty() and self._execute_plan_queue.empty():
                input_action: SimulationAction = self._api_to_sim_queue.get()
                input_action.set_reply_queue(self._sim_to_api_queue)
            # check for execute plan processing inputs, overwriting API and user input
            if not self._execute_plan_queue.empty() and self._simulation_state.get_robot().is_available():
                input_action: RobotAction = self._execute_plan_queue.get()
                input_action.set_reply_queue(self._execute_plan_reply_queue)
                self._current_execute_plan_action.increment_step()
            # process input action (if any)
            constraint_manager.validate_action(input_action, self._simulation_state) if input_action else None
            # handle action (if any)
            self._handle_action(input_action)
            # update robot state (if simulation is running)
            self._simulation_state.get_robot().update_state() if self._simulation_state.get_simulation_running() else None
            # log local reply queue
            self._log_local_reply_queue()
            # handle execute plan reply queue
            self._handle_execute_plan_reply_queue()
            # draw the simulation
            self._draw() if not self._verification_mode else None
            # update clock
            self._clock.tick(self._fps)
        # if we reach here, it means the app should quitting, so quit pygame, app will be closed by main.py
        pygame.quit()
        return