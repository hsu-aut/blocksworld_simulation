from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class InitialState(BaseModel):
    stacks: List[List[str]]
    holding: Optional[str] = None
    robot_status: str = "idle"


class Goal(BaseModel):
    description: str
    target_stacks: List[List[str]]
    
    
class Scenario(BaseModel):
    name: str
    description: str
    initial_state: InitialState
    goal: Goal
    metadata: Optional[Dict[str, Any]] = None