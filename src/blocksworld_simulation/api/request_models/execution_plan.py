from typing import Optional, Union, Literal
from pydantic import BaseModel


LETTERS = Literal[
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z"
]

class UnstackStep(BaseModel):
    """Pydantic model for an unstack step in the execution plan."""
    action: str = "unstack"
    block1: LETTERS
    block2: LETTERS


class StackStep(BaseModel):
    """Pydantic model for a stack step in the execution plan."""
    action: str = "stack"
    block1: LETTERS
    block2: LETTERS


class PickUpStep(BaseModel):
    """Pydantic model for a pick up step in the execution plan."""
    action: str = "pick_up"
    block: LETTERS


class PutDownStep(BaseModel):
    """Pydantic model for a put down step in the execution plan."""
    action: str = "put_down"
    block: LETTERS


class ExecutePlanRequest(BaseModel):
    """Pydantic model for an execute plan request."""
    plan: list[Union[PickUpStep, PutDownStep, StackStep, UnstackStep]]
    """The execution plan to be executed."""   
    validation: Optional[bool] = False
    """If True, the plan will be executed instantly, with no graphical representation 
    and no modification of the simulatio state.
    The first error will be reported or none if the simulation is valid.
    If False (default), the plan will be executed in real-time."""