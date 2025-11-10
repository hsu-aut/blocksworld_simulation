from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet
from blocksworld_simulation.constraints.contraint_sets.different_blocks.different_blocks_rules import get_additional_rules
from blocksworld_simulation.constraints.contraint_sets.different_blocks.valid_start_config import ValidStartConfig
from blocksworld_simulation.constraints.contraint_sets.different_blocks.upper_block_narrower import UpperBlockNarrower


class DifferentBlocksConstraintSet(BaseConstraintSet):
    """Constraint set for the hanoi towers problem."""

    def __init__(self):
        super().__init__()
        # START: add ValidStartConfig
        self._start_constraints.extend([
            ValidStartConfig()
        ])
        # STACK: add BlockBelowWider
        self._stack_constraints.extend([
            UpperBlockNarrower()
        ])
        # Rules: first explain the hanoi towers problem, then add the base blocksworld rules
        self._rules = get_additional_rules() + self._rules

