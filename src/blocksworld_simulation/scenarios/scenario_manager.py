import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

from .scenario_models import Scenario

logger = logging.getLogger(__name__)


class ScenarioManager:
    def __init__(self):
        self.scenarios_dir = Path(__file__).parent / "definitions"
        self._scenarios_cache: Dict[str, Scenario] = {}
        self._load_scenarios()
    
    def _load_scenarios(self):
        """Load all scenario definitions from the definitions directory."""
        self._scenarios_cache.clear()
        
        if not self.scenarios_dir.exists():
            logger.warning(f"Scenarios directory not found: {self.scenarios_dir}")
            return
            
        for file_path in self.scenarios_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    scenario_data = json.load(f)
                    scenario = Scenario(**scenario_data)
                    self._scenarios_cache[scenario.name] = scenario
                    logger.info(f"Loaded scenario: {scenario.name} (ID: {scenario.id})")
            except Exception as e:
                logger.error(f"Failed to load scenario from {file_path}: {e}")
    
    def get_scenario_names(self) -> List[str]:
        """Get list of all available scenario names."""
        return list(self._scenarios_cache.keys())
    
    def get_scenario(self, identifier: str) -> Optional[Scenario]:
        """Get a specific scenario by name or ID."""
        # First try by ID 
        for scenario in self._scenarios_cache.values():
            if scenario.id == identifier:
                return scenario
            
        # Then try by name (backward compatibility)
        scenario = self._scenarios_cache.get(identifier)
        if scenario:
            return scenario
        
        return None
    
    def scenario_exists(self, identifier: str) -> bool:
        """Check if a scenario exists by name or ID."""
        return self.get_scenario(identifier) is not None
    
    def get_scenario_ids(self) -> List[str]:
        """Get list of all available scenario IDs."""
        return [scenario.id for scenario in self._scenarios_cache.values()]
    
    def reload_scenarios(self):
        """Reload all scenarios from disk."""
        self._load_scenarios()
    
    def get_scenario_info(self, scenario_name: Optional[str] = None):
        """Handle scenario requests - returns all scenarios if no name provided, specific scenario otherwise."""
        if scenario_name is None:
            # Return all scenarios
            scenarios = []
            for name in self.get_scenario_names():
                scenario = self.get_scenario(name)
                if scenario:
                    scenarios.append(scenario.model_dump())
            return {"scenarios": scenarios}
        else:
            # Return specific scenario
            scenario = self.get_scenario(scenario_name)
            if not scenario:
                return None
            return scenario.model_dump()


scenario_manager = ScenarioManager()