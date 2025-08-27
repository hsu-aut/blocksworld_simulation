from blocksworld_simulation.constraints.constraint_set import ConstraintSet
from blocksworld_simulation.constraints.contraint_sets.base.base_rules import get_base_rules
from blocksworld_simulation.constraints.contraint_sets.base.robot_holding import RobotHolding
from blocksworld_simulation.constraints.contraint_sets.base.robot_idle import RobotIdle
from blocksworld_simulation.constraints.contraint_sets.base.simulation_not_running import SimulationNotRunning
from blocksworld_simulation.constraints.contraint_sets.base.simulation_running import SimulationRunning
from blocksworld_simulation.constraints.contraint_sets.base.block_exists import BlockExists
from blocksworld_simulation.constraints.contraint_sets.base.robot_holding_specific_block import RobotHoldingSpecificBlock
from blocksworld_simulation.constraints.contraint_sets.base.only_block_in_stack import OnlyBlockInStack
from blocksworld_simulation.constraints.contraint_sets.base.block_on_top_of_stack import BlockOnTopOfStack
from blocksworld_simulation.constraints.contraint_sets.base.free_stack_available import FreeStackAvailable
from blocksworld_simulation.constraints.contraint_sets.base.blocks_on_same_stack import BlocksOnSameStack
from blocksworld_simulation.constraints.contraint_sets.base.block_below_relationship import BlockBelowRelationship
from blocksworld_simulation.constraints.contraint_sets.base.unique_block_names import UniqueBlockNames
from blocksworld_simulation.constraints.contraint_sets.base.valid_start_data import ValidStartData

class BaseConstraintSet(ConstraintSet):
    """Constraint set for the basic blocks world problem."""

    def __init__(self):
        super().__init__()
        # QUIT: No constraints
        self._quit_constraints.extend([])
        # PRE START: SimulationNotRunning, ValidStartData
        self._pre_start_constraints.extend([
            SimulationNotRunning(),
            ValidStartData()
        ])
        # START: SimulationNotRunning, UniqueBlockNames
        self._start_constraints.extend([
            SimulationNotRunning(),
            UniqueBlockNames()
        ])
        # STOP: SimulationRunning
        self._stop_constraints.extend([
            SimulationRunning()
        ])
        # GET STATUS: SimulationRunning
        self._get_status_constraints.extend([
            SimulationRunning()
        ])
        # GET RULES: No constraints
        self._get_rules_constraints.extend([
            SimulationRunning()
        ])
        # PICK UP: SimulationRunning, RobotIdle, BlockExists, BlockOnGroundOnly, BlockOnTopOfStack
        self._pick_up_constraints.extend([
            SimulationRunning(),
            RobotIdle(),
            BlockExists(),
            BlockOnTopOfStack(),
            OnlyBlockInStack()
        ])
        # PUT DOWN: SimulationRunning, RobotHolding, BlockExists, RobotHoldingSpecificBlock, FreeStackAvailable
        self._put_down_constraints.extend([
            SimulationRunning(),
            RobotHolding(),
            BlockExists(),
            RobotHoldingSpecificBlock(),
            FreeStackAvailable()
        ])
        # STACK: SimulationRunning, RobotHolding, BlockExists, RobotHoldingSpecificBlock, BlockOnTopOfStack (target)
        self._stack_constraints.extend([
            SimulationRunning(),
            RobotHolding(),
            BlockExists(),
            RobotHoldingSpecificBlock(),
            BlockOnTopOfStack()
        ])
        # UNSTACK: SimulationRunning, RobotIdle, BlockExists, BlockOnTopOfStack, BlocksOnSameStack, BlockBelowRelationship
        self._unstack_constraints.extend([
            SimulationRunning(),
            RobotIdle(),
            BlockExists(),
            BlockOnTopOfStack(),
            BlocksOnSameStack(),
            BlockBelowRelationship()
        ])
        self._rules = get_base_rules()