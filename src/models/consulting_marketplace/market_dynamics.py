"""
Market Dynamics Module for Automotive Consulting

This module simulates the dynamics of the automotive consulting marketplace,
including demand trends, competitive landscape, and service evolution.
"""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional
import numpy as np
import pandas as pd


class ServiceType(Enum):
    """Types of consulting services in the automotive sector."""
    STRATEGY = "Strategy & Transformation"
    DIGITAL = "Digital & Technology"
    OPERATIONS = "Operations & Supply Chain"
    E_MOBILITY = "E-Mobility & Electrification"
    AUTONOMOUS = "Autonomous & Connected Vehicles"
    MOBILITY_SERVICES = "Mobility Services & Business Models"


class ClientType(Enum):
    """Types of clients in the automotive consulting market."""
    OEM = "Vehicle Manufacturers"
    TIER1 = "Tier 1 Suppliers"
    TIER2 = "Tier 2+ Suppliers"
    MOBILITY = "Mobility Service Providers"
    TECH = "Technology Companies"
    STARTUP = "Startups & New Entrants"


@dataclass
class ConsultingService:
    """Represents a consulting service offering."""
    service_type: ServiceType
    growth_rate: float  # Annual growth rate (0-1)
    market_size: float  # In $M
    competitive_intensity: float  # 0-1 scale
    key_competitors: List[str]
    
    def forecast_market_size(self, years: int = 5) -> float:
        """Forecast market size for given number of years."""
        return self.market_size * ((1 + self.growth_rate) ** years)


@dataclass
class ConsultingMarket:
    """Represents the automotive consulting market."""
    services: Dict[ServiceType, ConsultingService] = field(default_factory=dict)
    
    def add_service(self, service: ConsultingService) -> None:
        """Add a service to the market."""
        self.services[service.service_type] = service
    
    def get_market_size(self, service_type: Optional[ServiceType] = None) -> float:
        """Get total market size or for a specific service."""
        if service_type:
            return self.services[service_type].market_size
        return sum(s.market_size for s in self.services.values())
    
    def forecast_market(self, years: int = 5) -> Dict[ServiceType, float]:
        """Forecast market size for all services."""
        return {
            service_type: service.forecast_market_size(years)
            for service_type, service in self.services.items()
        }


def create_sample_market() -> ConsultingMarket:
    """Create a sample consulting market with realistic data."""
    market = ConsultingMarket()
    
    # Add sample services
    market.add_service(ConsultingService(
        service_type=ServiceType.E_MOBILITY,
        growth_rate=0.15,
        market_size=3500.0,  # $3.5B
        competitive_intensity=0.7,
        key_competitors=["McKinsey", "BCG", "Roland Berger", "PwC"]
    ))
    
    market.add_service(ConsultingService(
        service_type=ServiceType.AUTONOMOUS,
        growth_rate=0.25,
        market_size=2800.0,  # $2.8B
        competitive_intensity=0.8,
        key_competitors=["McKinsey", "BCG", "Deloitte", "Accenture"]
    ))
    
    market.add_service(ConsultingService(
        service_type=ServiceType.MOBILITY_SERVICES,
        growth_rate=0.18,
        market_size=2200.0,  # $2.2B
        competitive_intensity=0.65,
        key_competitors=["BCG", "Roland Berger", "McKinsey", "EY"]
    ))
    
    return market
