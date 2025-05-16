"""
Chinese Vehicle Manufacturer Global Expansion Simulation (2025-2040)

This module simulates the global expansion of Chinese automakers and its impact on the automotive industry.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass
import os
from pathlib import Path

# --- Enums and Data Classes ---

class Region(Enum):
    """Geographic regions for market analysis."""
    NORTH_AMERICA = auto()
    EUROPE = auto()
    CHINA = auto()
    JAPAN_KOREA = auto()
    EMERGING_MARKETS = auto()
    LATIN_AMERICA = auto()
    MIDDLE_EAST_AFRICA = auto()
    SOUTH_ASIA = auto()
    OCEANIA = auto()

class MarketSegment(Enum):
    """Vehicle market segments."""
    ENTRY = auto()
    MASS_MARKET = auto()
    PREMIUM = auto()
    LUXURY = auto()
    COMMERCIAL = auto()
    EV = auto()

class ChineseManufacturer(Enum):
    """Major Chinese automotive manufacturers."""
    SAIC = auto()
    GEELY = auto()
    BYD = auto()
    CHERY = auto()
    GREAT_WALL = auto()
    NIO = auto()
    XPENG = auto()
    LI_AUTO = auto()
    CHANGAN = auto()
    GAC = auto()

class ExpansionStrategy(Enum):
    """Global expansion strategies for Chinese manufacturers."""
    EXPORT = auto()
    LOCAL_PRODUCTION = auto()
    ACQUISITION = auto()
    JOINT_VENTURE = auto()
    BRAND_ACQUISITION = auto()

@dataclass
class MarketEntry:
    """Represents a market entry by a Chinese manufacturer."""
    manufacturer: ChineseManufacturer
    region: Region
    segment: MarketSegment
    entry_year: int
    strategy: ExpansionStrategy
    initial_market_share: float
    growth_rate: float

# --- Core Simulation Class ---

class ChineseExpansionSimulator:
    """Simulates the global expansion of Chinese automotive manufacturers."""
    
    def __init__(self):
        # Initialize market conditions by region
        self.market_conditions = {
            region: {
                'market_size': 1.0,  # Relative market size
                'growth_rate': 0.02,  # Annual growth rate
                'barriers_to_entry': 0.5,  # 0-1 scale, higher = more difficult
                'preference_domestic': 0.6,  # Preference for domestic brands
                'ev_penetration': 0.1,  # Current EV market share
                'ev_growth': 0.15,  # Annual EV market share growth
            }
            for region in Region
        }
        
        # Set specific regional parameters
        self._set_regional_parameters()
        
        # Initialize Chinese manufacturers with their strategies
        self.manufacturers = self._initialize_manufacturers()
    
    def _set_regional_parameters(self):
        """Set specific parameters for each region."""
        # China
        self.market_conditions[Region.CHINA].update({
            'market_size': 1.5,
            'growth_rate': 0.04,
            'barriers_to_entry': 0.2,
            'preference_domestic': 0.8,
            'ev_penetration': 0.25,
            'ev_growth': 0.2,
        })
        
        # North America
        self.market_conditions[Region.NORTH_AMERICA].update({
            'market_size': 1.2,
            'growth_rate': 0.01,
            'barriers_to_entry': 0.7,
            'preference_domestic': 0.7,
            'ev_penetration': 0.08,
            'ev_growth': 0.12,
        })
        
        # Europe
        self.market_conditions[Region.EUROPE].update({
            'market_size': 1.1,
            'growth_rate': 0.005,
            'barriers_to_entry': 0.6,
            'preference_domestic': 0.65,
            'ev_penetration': 0.15,
            'ev_growth': 0.18,
        })
        
        # Emerging Markets
        self.market_conditions[Region.EMERGING_MARKETS].update({
            'market_size': 0.8,
            'growth_rate': 0.06,
            'barriers_to_entry': 0.4,
            'preference_domestic': 0.4,
            'ev_penetration': 0.02,
            'ev_growth': 0.25,
        })
    
    def _initialize_manufacturers(self) -> Dict[ChineseManufacturer, dict]:
        """Initialize Chinese manufacturers with their strategies and capabilities."""
        return {
            ChineseManufacturer.BYD: {
                'name': 'BYD',
                'strengths': [MarketSegment.EV, MarketSegment.MASS_MARKET],
                'global_presence': {Region.CHINA: 0.15},  # Initial market share in home market
                'ev_tech_level': 0.9,  # 0-1 scale
                'brand_value': 0.7,  # 0-1 scale
                'production_capacity': 1.0,  # Relative capacity
                'rnd_investment': 0.8,  # 0-1 scale
            },
            ChineseManufacturer.GEELY: {
                'name': 'Geely',
                'strengths': [MarketSegment.MASS_MARKET, MarketSegment.PREMIUM],
                'global_presence': {Region.CHINA: 0.12, Region.EUROPE: 0.02},
                'ev_tech_level': 0.7,
                'brand_value': 0.75,
                'production_capacity': 1.2,
                'rnd_investment': 0.75,
                'acquisitions': ['Volvo', 'Lotus', 'Proton', 'Lynk & Co']
            },
            ChineseManufacturer.NIO: {
                'name': 'NIO',
                'strengths': [MarketSegment.PREMIUM, MarketSegment.EV],
                'global_presence': {Region.CHINA: 0.05, Region.EUROPE: 0.01},
                'ev_tech_level': 0.95,
                'brand_value': 0.8,
                'production_capacity': 0.6,
                'rnd_investment': 0.9,
            },
            ChineseManufacturer.XPENG: {
                'name': 'XPeng',
                'strengths': [MarketSegment.EV, MarketSegment.MASS_MARKET],
                'global_presence': {Region.CHINA: 0.04, Region.EUROPE: 0.005},
                'ev_tech_level': 0.85,
                'brand_value': 0.65,
                'production_capacity': 0.5,
                'rnd_investment': 0.85,
            },
            ChineseManufacturer.SAIC: {
                'name': 'SAIC Motor',
                'strengths': [MarketSegment.MASS_MARKET, MarketSegment.COMMERCIAL],
                'global_presence': {Region.CHINA: 0.18, Region.EMERGING_MARKETS: 0.03},
                'ev_tech_level': 0.7,
                'brand_value': 0.6,
                'production_capacity': 1.5,
                'rnd_investment': 0.7,
                'joint_ventures': ['MG', 'Roewe', 'Maxus']
            }
        }
    
    def calculate_market_attractiveness(self, region: Region, segment: MarketSegment) -> float:
        """Calculate the attractiveness of a market segment in a region."""
        conditions = self.market_conditions[region]
        
        # Base attractiveness factors
        attractiveness = (
            conditions['market_size'] * 0.3 +
            conditions['growth_rate'] * 20 * 0.3 +  # Scale growth rate
            (1 - conditions['barriers_to_entry']) * 0.2 +
            (1 - conditions['preference_domestic']) * 0.2
        )
        
        # Adjust for EV segment
        if segment == MarketSegment.EV:
            attractiveness *= (1 + conditions['ev_penetration'] * 2)
            attractiveness *= (1 + conditions['ev_growth'] * 5)
        
        return attractiveness
    
    def simulate_expansion(
        self,
        start_year: int = 2025,
        end_year: int = 2040,
        regions: Optional[List[Region]] = None,
        segments: Optional[List[MarketSegment]] = None
    ) -> Dict:
        """Simulate the global expansion of Chinese manufacturers."""
        if regions is None:
            regions = list(Region)
        if segments is None:
            segments = list(MarketSegment)
        
        years = list(range(start_year, end_year + 1))
        results = {
            'market_share': {mfg: {r: {s: [] for s in segments} for r in regions} 
                           for mfg in self.manufacturers},
            'revenue': {mfg: {r: {s: [] for s in segments} for r in regions} 
                      for mfg in self.manufacturers},
            'strategy': {mfg: {r: {s: [] for s in segments} for r in regions} 
                       for mfg in self.manufacturers}
        }
        
        for year in years:
            for region in regions:
                for segment in segments:
                    # Calculate market size for this year, region, and segment
                    market_size = self._calculate_market_size(year, region, segment)
                    
                    # Update each manufacturer's position
                    for mfg, mfg_data in self.manufacturers.items():
                        # Skip if manufacturer not in this segment
                        if segment not in mfg_data['strengths'] and segment != MarketSegment.EV:
                            continue
                            
                        # Determine expansion strategy
                        strategy = self._determine_strategy(mfg, region, segment, year)
                        
                        # Calculate market share based on strategy and competition
                        market_share = self._calculate_market_share(
                            mfg, region, segment, year, strategy, market_size
                        )
                        
                        # Update manufacturer's presence
                        if region not in mfg_data['global_presence']:
                            mfg_data['global_presence'][region] = 0.0
                        mfg_data['global_presence'][region] = market_share
                        
                        # Calculate revenue (simplified)
                        revenue = market_size * market_share * self._get_price_multiplier(segment)
                        
                        # Store results
                        results['market_share'][mfg][region][segment].append(market_share)
                        results['revenue'][mfg][region][segment].append(revenue)
                        results['strategy'][mfg][region][segment].append(strategy.name)
        
        # Save results
        self._save_results(results, years, regions, segments)
        
        return results
    
    def _calculate_market_size(self, year: int, region: Region, segment: MarketSegment) -> float:
        """Calculate the market size for a given year, region, and segment."""
        base_size = self.market_conditions[region]['market_size']
        growth_rate = self.market_conditions[region]['growth_rate']
        years_from_base = year - 2025
        
        # Adjust for EV segment
        if segment == MarketSegment.EV:
            ev_penetration = min(
                self.market_conditions[region]['ev_penetration'] * 
                (1 + self.market_conditions[region]['ev_growth']) ** years_from_base,
                0.9  # Max 90% penetration
            )
            return base_size * (1 + growth_rate) ** years_from_base * ev_penetration
        else:
            return base_size * (1 + growth_rate) ** years_from_base * 0.2  # Simplified
    
    def _determine_strategy(
        self, 
        manufacturer: ChineseManufacturer, 
        region: Region, 
        segment: MarketSegment,
        year: int
    ) -> ExpansionStrategy:
        """Determine the best expansion strategy for a manufacturer in a given market."""
        mfg_data = self.manufacturers[manufacturer]
        
        # If already present, continue with existing strategy or optimize
        if region in mfg_data['global_presence'] and mfg_data['global_presence'][region] > 0.01:
            # Consider switching to local production if volume justifies it
            if mfg_data['global_presence'][region] > 0.05 and year > 2030:
                return ExpansionStrategy.LOCAL_PRODUCTION
            return ExpansionStrategy.EXPORT
        
        # For new market entry
        barriers = self.market_conditions[region]['barriers_to_entry']
        
        if barriers > 0.7:
            # High barriers - consider JV or acquisition
            if 'acquisitions' in mfg_data and len(mfg_data['acquisitions']) > 0:
                return ExpansionStrategy.ACQUISITION
            return ExpansionStrategy.JOINT_VENTURE
        elif barriers > 0.4:
            # Medium barriers - consider brand acquisition
            return ExpansionStrategy.BRAND_ACQUISITION
        else:
            # Low barriers - start with exports
            return ExpansionStrategy.EXPORT
    
    def _calculate_market_share(
        self,
        manufacturer: ChineseManufacturer,
        region: Region,
        segment: MarketSegment,
        year: int,
        strategy: ExpansionStrategy,
        market_size: float
    ) -> float:
        """Calculate market share based on various factors."""
        mfg_data = self.manufacturers[manufacturer]
        current_share = mfg_data['global_presence'].get(region, 0.0)
        
        # Base growth factor
        growth_factor = 0.05  # Base growth
        
        # Adjust based on strategy
        if strategy == ExpansionStrategy.LOCAL_PRODUCTION:
            growth_factor += 0.1
        elif strategy == ExpansionStrategy.ACQUISITION:
            growth_factor += 0.15
        elif strategy == ExpansionStrategy.JOINT_VENTURE:
            growth_factor += 0.08
        elif strategy == ExpansionStrategy.BRAND_ACQUISITION:
            growth_factor += 0.12
        
        # Adjust for EV advantage
        if segment == MarketSegment.EV and mfg_data['ev_tech_level'] > 0.8:
            growth_factor += 0.1
        
        # Adjust for brand value
        growth_factor *= mfg_data['brand_value']
        
        # Calculate new market share with diminishing returns
        max_share = 0.4  # Maximum share a single manufacturer can achieve
        potential_share = min(current_share * (1 + growth_factor), max_share)
        
        # Adjust for market conditions
        market_attractiveness = self.calculate_market_attractiveness(region, segment)
        potential_share *= (market_attractiveness / 2.0)  # Normalize
        
        return min(potential_share, max_share)
    
    def _get_price_multiplier(self, segment: MarketSegment) -> float:
        """Get price multiplier for revenue calculation."""
        return {
            MarketSegment.ENTRY: 1.0,
            MarketSegment.MASS_MARKET: 1.2,
            MarketSegment.PREMIUM: 1.8,
            MarketSegment.LUXURY: 3.0,
            MarketSegment.COMMERCIAL: 2.5,
            MarketSegment.EV: 1.5
        }.get(segment, 1.0)
    
    def _save_results(
        self, 
        results: Dict, 
        years: List[int],
        regions: List[Region],
        segments: List[MarketSegment]
    ) -> None:
        """Save simulation results to CSV files."""
        # Define output directory using absolute path
        script_dir = Path(__file__).parent.parent.parent.parent  # Go up to project root
        output_dir = script_dir / 'data' / 'processed_data' / 'chinese_expansion'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save market share data
        share_data = []
        for mfg in self.manufacturers:
            for region in regions:
                for segment in segments:
                    for year, share in zip(years, results['market_share'][mfg][region][segment]):
                        if share > 0:  # Only include non-zero entries
                            share_data.append({
                                'year': year,
                                'manufacturer': mfg.name,
                                'region': region.name,
                                'segment': segment.name,
                                'market_share': share,
                                'revenue_millions': results['revenue'][mfg][region][segment][year - years[0]],
                                'strategy': (
                                    results['strategy'][mfg][region][segment][year - years[0]].name 
                                    if hasattr(results['strategy'][mfg][region][segment][year - years[0]], 'name')
                                    else str(results['strategy'][mfg][region][segment][year - years[0]])
                                    if results['strategy'][mfg][region][segment][year - years[0]] is not None 
                                    else 'N/A'
                                )
                            })
        
        # Convert to DataFrame and save
        df = pd.DataFrame(share_data)
        output_file = output_dir / 'market_share_evolution.csv'
        df.to_csv(output_file, index=False)
        print(f"Saved market share evolution data to: {output_file}")
        
        # Also save a summary by region and manufacturer
        if len(share_data) > 0:
            summary_df = df.groupby(['year', 'region', 'manufacturer'])['market_share'].sum().unstack().reset_index()
            summary_file = output_dir / 'market_share_summary.csv'
            summary_df.to_csv(summary_file, index=False)
            print(f"Saved market share summary to: {summary_file}")


def run_chinese_expansion_simulation(
    start_year: int = 2025,
    end_year: int = 2040,
    regions: Optional[Union[List[Union[str, Region]], str]] = None,
    segments: Optional[Union[List[Union[str, MarketSegment]], str]] = None
) -> Dict:
    """Run the Chinese manufacturer expansion simulation.
    
    Args:
        start_year: Start year of the simulation (default: 2025)
        end_year: End year of the simulation (default: 2040)
        regions: List of regions (as strings or Region enums) or 'all' for all regions
        segments: List of market segments (as strings or MarketSegment enums) or 'all' for all segments
        
    Returns:
        Dictionary containing simulation results with market share, revenue, and strategy data
    """
    # Convert string inputs to enums if needed
    if regions == 'all' or regions is None:
        region_enums = list(Region)
    else:
        region_enums = []
        for r in regions if isinstance(regions, list) else [regions]:
            if isinstance(r, str):
                try:
                    region_enums.append(Region[r.upper()])
                except KeyError:
                    raise ValueError(f"Invalid region: {r}. Valid regions are: {[e.name for e in Region]}")
            else:
                region_enums.append(r)
    
    if segments == 'all' or segments is None:
        segment_enums = list(MarketSegment)
    else:
        segment_enums = []
        for s in segments if isinstance(segments, list) else [segments]:
            if isinstance(s, str):
                try:
                    segment_enums.append(MarketSegment[s.upper()])
                except KeyError:
                    raise ValueError(f"Invalid segment: {s}. Valid segments are: {[e.name for e in MarketSegment]}")
            else:
                segment_enums.append(s)
    
    simulator = ChineseExpansionSimulator()
    return simulator.simulate_expansion(start_year, end_year, region_enums, segment_enums)


def plot_chinese_expansion_results(results: Dict, save_path: str = None) -> None:
    """Plot the results of the Chinese expansion simulation."""
    # This would be implemented to create visualizations
    pass


if __name__ == "__main__":
    print("Running Chinese Vehicle Manufacturer Global Expansion Simulation (2025-2040)...")
    
    # Run the simulation
    results = run_chinese_expansion_simulation(2025, 2040)
    
    # Generate visualizations
    plot_chinese_expansion_results(results)
    
    print("Simulation completed. Results saved to data/processed_data/chinese_expansion/")
