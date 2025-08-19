from flask import request, jsonify
from pydantic import BaseModel, ValidationError, field_validator, model_validator
from typing import List, Optional, Union
import re
from ..simulation.block import BlockModel

class StartSimulationRequest(BaseModel):
    """Pydantic model for starting the simulation with custom initial stacks.
    
    Examples:
    ```
    // Start with predefined scenario (query parameter)
    POST /start_simulation?scenario=tower_building_challenge
    // Body: {} or empty
    ```
    
    ```
    // Start with custom initial stacks (simple format)
    POST /start_simulation
    // Body:
    { 
        "initial_stacks": 
            [
                ["A", "B"], 
                [], 
                ["C"]
            ]
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
                    {"name": "A", "x_size": 50, "y_size": 30, "weight": 10, "type": "X"},
                    {"name": "B", "x_size": 50, "y_size": 30, "weight": 10, "type": "X2"}
                ],
                [],
                [
                    {"name": "C", "x_size": 50, "y_size": 30, "weight": 10, "type": "s98"}
                ]
            ]
    }
    ```
        """
    initial_stacks: Optional[
        List[
            List[
                Union[str, BlockModel]
            ]
        ]
    ] = None
    
    @model_validator(mode='after')
    def validate_unique_block_names(self):
        # Validate unique block names if initial_stacks provided
        if self.initial_stacks:
            block_names = []
            for stack in self.initial_stacks:
                for block in stack:
                    name = block if isinstance(block, str) else block.name
                    if name in block_names:
                        raise ValueError(f'Block name "{name}" appears multiple times. Each block must have a unique name.')
                    block_names.append(name)
        return self

class PickUpRequest(BaseModel):
    block: str
    
    @field_validator('block')
    @classmethod
    def validate_block_name(cls, v):
        if not re.match(r'^[A-Z]$', v):
            raise ValueError('Block name must be a single uppercase letter A-Z')
        return v

class PutDownRequest(BaseModel):
    block: str
    
    @field_validator('block')
    @classmethod
    def validate_block_name(cls, v):
        if not re.match(r'^[A-Z]$', v):
            raise ValueError('Block name must be a single uppercase letter A-Z')
        return v

class StackRequest(BaseModel):
    block1: str
    block2: str
    
    @field_validator('block1', 'block2')
    @classmethod
    def validate_block_names(cls, v):
        if not re.match(r'^[A-Z]$', v):
            raise ValueError('Block name must be a single uppercase letter A-Z')
        return v

class UnstackRequest(BaseModel):
    block1: str
    block2: str
    
    @field_validator('block1', 'block2')
    @classmethod
    def validate_block_names(cls, v):
        if not re.match(r'^[A-Z]$', v):
            raise ValueError('Block name must be a single uppercase letter A-Z')
        return v

def validate_request(request_model, allow_empty_body=False):
    """Decorator to validate JSON requests using Pydantic models."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if allow_empty_body and request.content_length == 0:
                return func(None, *args, **kwargs)
            try:
                data = request.get_json()
                if data is None:
                    return jsonify({"error": "No JSON data provided"}), 400
                validated_data = request_model(**data)
                return func(validated_data, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"errors": e.errors()}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator