from typing import Literal
from pydantic import BaseModel


LETTERS = Literal[
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z"
]

class UnstackStep(BaseModel):
    """Pydantic model for an unstack step in the execution plan."""
    action: Literal["unstack"]
    block1: LETTERS
    block2: LETTERS


class StackStep(BaseModel):
    """Pydantic model for a stack step in the execution plan."""
    action: Literal["stack"]
    block1: LETTERS
    block2: LETTERS


class PickUpStep(BaseModel):
    """Pydantic model for a pick up step in the execution plan."""
    action: Literal["pick_up"]
    block: LETTERS


class PutDownStep(BaseModel):
    """Pydantic model for a put down step in the execution plan."""
    action: Literal["put_down"]
    block: LETTERS


class PlanRequest(BaseModel):
    """Pydantic model for an execute plan request."""
    plan: list[UnstackStep | StackStep | PickUpStep | PutDownStep]
    """The execution plan to be executed."""