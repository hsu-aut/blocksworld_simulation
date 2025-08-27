from pydantic import BaseModel
from typing import List, Optional, Union
from ...simulation.block import BlockModel


class StartSimulationRequest(BaseModel):
    """Pydantic model for starting the simulation.
    
    Two modes supported:
    1. Direct configuration with custom stacks and optional constraint set
    2. Scenario-based configuration (constraint set from scenario)
    
    Examples:
    ```
    // Start with predefined scenario
    POST /start_simulation
    // Body:
    { 
        "scenario_id": "unstacking_challenge"
    }
    ```
    
    ```
    // Start with custom initial stacks (defaults to base constraint set)
    POST /start_simulation
    // Body:
    { 
        "initial_stacks": [["A", "B"], [], ["C"]]
    }
    ```
    
    ```
    // Start with custom initial stacks and specific constraint set
    POST /start_simulation
    // Body:
    { 
        "initial_stacks": [["A", "B"], [], ["C"]],
        "constraint_set": "hanoi_towers"
    }
    ```
    
    ```
    // Start with custom initial stacks (detailed format)
    POST /start_simulation
    // Body:
    { 
        "initial_stacks": 
        [
            [
                {"name": "D", "x_size": 100, "y_size": 30},
                {"name": "C", "x_size": 80, "y_size": 30},
                {"name": "B", "x_size": 60, "y_size": 30},
                {"name": "A", "x_size": 40, "y_size": 30}
            ],
            [],
            []
        ],
        "constraint_set": "hanoi_towers"
    }
    ```
    """
    scenario_id: Optional[str] = None
    initial_stacks: Optional[
        List[
            List[
                Union[str, BlockModel]
            ]
        ]
    ] = None
    constraint_set: Optional[str] = None
    
class StopSimulationRequest(BaseModel):
    """Request model for stopping the simulation."""
    pass