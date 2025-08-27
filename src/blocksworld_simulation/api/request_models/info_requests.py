from pydantic import BaseModel
from typing import Optional


class GetScenarioRequest(BaseModel):
    """Request model for scenario-related operations."""
    scenario_name: Optional[str] = None


class GetStatusRequest(BaseModel):
    """Request model for getting simulation status."""
    pass


class GetRulesRequest(BaseModel):
    """Request model for getting simulation rules."""
    pass