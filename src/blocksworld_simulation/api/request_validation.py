from flask import request, jsonify
from pydantic import BaseModel, ValidationError, field_validator, model_validator
from typing import List, Optional, Union
import re

class BlockModel(BaseModel):
    name: str
    x_size: int
    y_size: int
    weight: int
    type: str
    
    @field_validator('name')
    @classmethod
    def validate_block_name(cls, v):
        if not re.match(r'^[A-Z]$', v):
            raise ValueError('Block name must be a single uppercase letter A-Z')
        return v

class StartSimulationRequest(BaseModel):
    """Pydantic model for starting the simulation.
    Request body should contain initial stacks or empty for default.
    If Initial stacks are provided, the request body should look like:
    ```
    { 
        "initial_stacks": 
            [
                ["A", "B"], 
                [], 
                ["C"]
            ]
    }
    ```
    or, fully defined:
    ```
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

def validate_request(request_model):
    """Decorator to validate JSON requests using Pydantic models."""
    def decorator(func):
        def wrapper(*args, **kwargs):
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