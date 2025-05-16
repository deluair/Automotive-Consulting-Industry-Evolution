"""
Market Scenarios for Automotive Consulting

This module defines various market scenarios for the automotive consulting industry,
including base case, optimistic, and pessimistic outlooks.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import numpy as np


class ScenarioType(Enum):
    """Types of market scenarios."""
    BASE = "Base Case"
    OPTIMISTIC = "Optimistic"
    PESSIMISTIC = "Pessimistic"
    DISRUPTION = "Market Disruption"
    TRANSFORMATION = "Accelerated Transformation"


class MarketDriver(Enum):
    """Key drivers of the automotive consulting market."""
    EV_ADOPTION = "EV Adoption Rate"
    AUTONOMOUS_TECH = "Autonomous Technology Development"
    REGULATORY_CHANGE = "Regulatory Changes"
    ECONOMIC_GROWTH = "Global Economic Growth"
    TECH_INVESTMENT = "Technology Investment Levels"
    CONSUMER_BEHAVIOR = "Consumer Behavior Shifts"


@dataclass
class ScenarioParameter:
    """Parameter for a market scenario."""
    name: str
    base_value: float
    optimistic_value: float
    pessimistic_value: float
    unit: str = ""
    description: str = ""


@dataclass
class MarketScenario:
    """Represents a market scenario for the automotive consulting industry."""
    name: str
    scenario_type: ScenarioType
    time_horizon: int = 5  # years
    probability: float = 1.0  # 0-1
    parameters: Dict[str, ScenarioParameter] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default parameters for the scenario."""
        self.parameters = {
            "ev_adoption_rate": ScenarioParameter(
                name="EV Adoption Rate",
                base_value=0.25,
                optimistic_value=0.4,
                pessimistic_value=0.15,
                unit="% of new car sales",
                description="Annual growth rate of EV adoption"
            ),
            "autonomous_tech_advancement": ScenarioParameter(
                name="Autonomous Tech Advancement",
                base_value=0.3,
                optimistic_value=0.5,
                pessimistic_value=0.1,
                unit="0-1 scale",
                description="Rate of advancement in autonomous technology"
            ),
            "consulting_budget_growth": ScenarioParameter(
                name="Consulting Budget Growth",
                base_value=0.05,
                optimistic_value=0.1,
                pessimistic_value=-0.02,
                unit="% annual growth",
                description="Annual growth in consulting budgets"
            )
        }
    
    def get_parameter_value(self, param_name: str) -> float:
        """Get the parameter value based on scenario type."""
        param = self.parameters.get(param_name)
        if not param:
            raise ValueError(f"Unknown parameter: {param_name}")
        
        if self.scenario_type == ScenarioType.OPTIMISTIC:
            return param.optimistic_value
        elif self.scenario_type == ScenarioType.PESSIMISTIC:
            return param.pessimistic_value
        else:  # BASE and others use base value
            return param.base_value
    
    def calculate_market_size(self, base_market_size: float) -> Dict[int, float]:
        """Calculate market size over the scenario's time horizon."""
        growth_rate = self.get_parameter_value("consulting_budget_growth")
        return {
            year: base_market_size * ((1 + growth_rate) ** (year - 2025))
            for year in range(2025, 2025 + self.time_horizon + 1)
        }


def create_scenario_bundle() -> Dict[str, MarketScenario]:
    """Create a bundle of standard market scenarios."""
    return {
        "base_case": MarketScenario(
            name="Base Case - Gradual Evolution",
            scenario_type=ScenarioType.BASE,
            probability=0.6
        ),
        "optimistic": MarketScenario(
            name="Optimistic - Accelerated Transformation",
            scenario_type=ScenarioType.OPTIMISTIC,
            probability=0.2
        ),
        "pessimistic": MarketScenario(
            name="Pessimistic - Constrained Growth",
            scenario_type=ScenarioType.PESSIMISTIC,
            probability=0.2
        )
    }


class ScenarioAnalyzer:
    """Analyzes and compares different market scenarios."""
    
    def __init__(self, scenarios: Dict[str, MarketScenario]):
        self.scenarios = scenarios
    
    def compare_parameter(self, param_name: str) -> Dict[str, float]:
        """Compare a parameter across all scenarios."""
        return {
            scenario_name: scenario.get_parameter_value(param_name)
            for scenario_name, scenario in self.scenarios.items()
        }
    
    def sensitivity_analysis(self, base_market_size: float) -> Dict[str, Dict[int, float]]:
        """Perform sensitivity analysis on market size across scenarios."""
        return {
            scenario_name: scenario.calculate_market_size(base_market_size)
            for scenario_name, scenario in self.scenarios.items()
        }
