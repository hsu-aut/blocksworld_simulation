from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import uuid

from blocksworld_simulation.simulation.block import BlockModel


class InitialState(BaseModel):
    stacks: List[List[Union[str, BlockModel]]] 
    holding: Optional[str] = None
    robot_status: str = "idle"


class Goal(BaseModel):
    description: str
    target_configurations: List[List[str]]
    
    
class Scenario(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    initial_state: InitialState
    goal: Goal
    constraint_set: str
    metadata: Optional[Dict[str, Any]] = None
    optimal_plan: Optional[List[Dict[str, Any]]] = None