from pydantic import BaseModel, field_validator
import re


def validate_block_name(v: str) -> str:
    """Validates that block name is a single uppercase letter A-Z"""
    if not re.match(r'^[A-Z]$', v):
        raise ValueError('Block name must be a single uppercase letter A-Z')
    return v


def create_block_name_validator(*field_names):
    """Creates a field validator for block names that can be applied to multiple fields"""
    return field_validator(*field_names)(classmethod(lambda cls, v: validate_block_name(v)))


class PickUpRequest(BaseModel):
    block: str
    validate_block = create_block_name_validator('block')


class PutDownRequest(BaseModel):
    block: str  
    validate_block = create_block_name_validator('block')


class StackRequest(BaseModel):
    block1: str
    block2: str
    validate_blocks = create_block_name_validator('block1', 'block2')


class UnstackRequest(BaseModel):
    block1: str
    block2: str    
    validate_blocks = create_block_name_validator('block1', 'block2')