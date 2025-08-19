from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class InitialState(BaseModel):
    stacks: List[List[str]]
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
    metadata: Optional[Dict[str, Any]] = None