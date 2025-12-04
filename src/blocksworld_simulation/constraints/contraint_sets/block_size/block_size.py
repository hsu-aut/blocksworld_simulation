from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet
from blocksworld_simulation.constraints.contraint_sets.block_size.block_size_rules import get_additional_rules
from blocksworld_simulation.constraints.contraint_sets.block_size.valid_start_config import ValidStartConfig
from blocksworld_simulation.constraints.contraint_sets.block_size.block_below_wider_equal import BlockBelowWiderEqual


class BlockSizeConstraintSet(BaseConstraintSet):
    """Constraint set for the hanoi towers problem."""

    def __init__(self):
        super().__init__()
        # START: add ValidStartConfig
        self._start_constraints.extend([
            ValidStartConfig()
        ])
        # STACK: add BlockBelowWider
        self._stack_constraints.extend([
            BlockBelowWiderEqual()
        ])
        # Rules: first explain the hanoi towers problem, then add the base blocksworld rules
        self._rules = get_additional_rules() + self._rules

