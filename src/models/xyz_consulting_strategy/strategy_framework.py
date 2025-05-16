"""
XYZ Consulting Strategy Framework

This module defines the strategic framework for XYZ Consulting to navigate
the automotive consulting market transformation.
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import numpy as np


class StrategicPillar(Enum):
    """Strategic pillars for XYZ Consulting."""
    TECHNOLOGY = "Technology & Innovation"
    TALENT = "Talent & Capabilities"
    CLIENT = "Client-Centric Solutions"
    OPERATIONS = "Operational Excellence"
    GROWTH = "Sustainable Growth"


class MarketPosition(Enum):
    """Possible market positions for consulting services."""
    LEADER = "Market Leader"
    CHALLENGER = "Challenger"
    FOLLOWER = "Follower"
    NICHE = "Niche Player"


@dataclass
class Capability:
    """Represents a strategic capability."""
    name: str
    current_strength: float  # 1-5 scale
    target_strength: float   # 1-5 scale
    priority: int            # 1 (highest) to 5 (lowest)
    
    def gap(self) -> float:
        """Calculate the capability gap."""
        return self.target_strength - self.current_strength


@dataclass
class StrategicObjective:
    """Represents a strategic objective."""
    name: str
    pillar: StrategicPillar
    description: str
    key_results: List[Tuple[str, float]]  # (metric, target_value)
    capabilities: List[Capability]
    
    def progress(self) -> float:
        """Calculate progress toward the objective (0-1)."""
        if not self.capabilities:
            return 0.0
        total_gap = sum(c.gap() for c in self.capabilities)
        max_gap = sum(5 - c.current_strength for c in self.capabilities)
        return 1 - (total_gap / max_gap) if max_gap > 0 else 1.0


class XYZStrategy:
    """XYZ Consulting's strategic framework."""
    
    def __init__(self):
        self.objectives: Dict[str, StrategicObjective] = {}
        self._init_strategy()
    
    def _init_strategy(self) -> None:
        """Initialize the strategic objectives."""
        # Technology & Innovation
        self.add_objective(StrategicObjective(
            name="Lead in Automotive Tech Consulting",
            pillar=StrategicPillar.TECHNOLOGY,
            description="Become the go-to consulting firm for automotive technology transformation",
            key_results=[
                ("Market Share in Tech Consulting", 0.25),  # 25%
                ("IP & Assets Developed", 15),  # Number of proprietary assets
                ("Tech Talent Headcount", 200)   # Number of tech specialists
            ],
            capabilities=[
                Capability("Digital Twin Expertise", 2, 5, 1),
                Capability("AI/ML in Automotive", 3, 5, 1),
                Capability("Software-Defined Vehicle", 1, 4, 2)
            ]
        ))
        
        # Client-Centric Solutions
        self.add_objective(StrategicObjective(
            name="Enhance Client Value Proposition",
            pillar=StrategicPillar.CLIENT,
            description="Develop industry-leading client solutions and delivery models",
            key_results=[
                ("Client Satisfaction Score", 4.5),  # out of 5
                ("Repeat Business Rate", 0.7),      # 70%
                ("Solution Innovation Index", 4.0)   # out of 5
            ],
            capabilities=[
                Capability("Solution Development", 3, 5, 1),
                Capability("Client Relationship Management", 4, 5, 2),
                Capability("Industry-Specific Knowledge", 3, 4, 2)
            ]
        ))
    
    def add_objective(self, objective: StrategicObjective) -> None:
        """Add a strategic objective."""
        self.objectives[objective.name] = objective
    
    def get_objective(self, name: str) -> Optional[StrategicObjective]:
        """Get a strategic objective by name."""
        return self.objectives.get(name)
    
    def get_objectives_by_pillar(self, pillar: StrategicPillar) -> List[StrategicObjective]:
        """Get all objectives for a specific pillar."""
        return [obj for obj in self.objectives.values() if obj.pillar == pillar]
    
    def overall_progress(self) -> float:
        """Calculate overall strategy progress (0-1)."""
        if not self.objectives:
            return 0.0
        return sum(obj.progress() for obj in self.objectives.values()) / len(self.objectives)


class StrategicInitiative:
    """Represents a strategic initiative to achieve objectives."""
    
    def __init__(self, 
                 name: str, 
                 objectives: List[str],
                 budget: float,
                 duration_months: int):
        self.name = name
        self.objectives = objectives
        self.budget = budget
        self.duration_months = duration_months
        self.progress = 0.0  # 0-1
        self.risks: List[Tuple[str, float]] = []  # (risk_description, probability)
    
    def update_progress(self, progress: float) -> None:
        """Update the initiative's progress (0-1)."""
        self.progress = max(0.0, min(1.0, progress))
    
    def add_risk(self, description: str, probability: float) -> None:
        """Add a risk to the initiative."""
        self.risks.append((description, probability))
