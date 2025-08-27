from blocksworld_simulation.constraints.contraint_sets.base.base import BaseConstraintSet
from blocksworld_simulation.constraints.contraint_sets.hanoi_towers.block_below_wider import BlockBelowWider


class HanoiTowersConstraintSet(BaseConstraintSet):
    """Constraint set for the hanoi towers problem."""

    def __init__(self):
        super().__init__()
        # QUIT: No additional constraints
        self._quit_constraints.extend([])
        # START: No additional constraints
        self._start_constraints.extend([])
        # STOP: No additional constraints
        self._stop_constraints.extend([])
        # GET STATUS: No additional constraints
        self._get_status_constraints.extend([])
        # PICK UP: No additional constraints
        self._pick_up_constraints.extend([])
        # PUT DOWN: No additional constraints
        self._put_down_constraints.extend([])
        # STACK: BlockBelowWider
        self._stack_constraints.extend([
            BlockBelowWider()
        ])
        # UNSTACK: No additional constraints
        self._unstack_constraints.extend([])

