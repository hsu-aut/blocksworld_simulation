import json
import os
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
                    logger.info(f"Loaded scenario: {scenario.name}")
            except Exception as e:
                logger.error(f"Failed to load scenario from {file_path}: {e}")
    
    def get_scenario_names(self) -> List[str]:
        """Get list of all available scenario names."""
        return list(self._scenarios_cache.keys())
    
    def get_scenario(self, name: str) -> Optional[Scenario]:
        """Get a specific scenario by name."""
        return self._scenarios_cache.get(name)
    
    def scenario_exists(self, name: str) -> bool:
        """Check if a scenario exists."""
        return name in self._scenarios_cache
    
    def reload_scenarios(self):
        """Reload all scenarios from disk."""
        self._load_scenarios()


scenario_manager = ScenarioManager()