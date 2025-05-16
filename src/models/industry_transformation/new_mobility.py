"""
New Mobility & Business Model Evolution Simulation (2025-2040)

This module simulates the transformation of mobility services, ownership models,
and revenue streams in the automotive industry.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from enum import Enum, auto
from dataclasses import dataclass
import random
import os
from pathlib import Path

# --- Enums and Data Classes ---

class MobilityServiceType(Enum):
    """Types of mobility services."""
    RIDE_HAILING = auto()
    CAR_SHARING = auto()
    ROBOTAXI = auto()
    SUBSCRIPTION = auto()

class OwnershipModel(Enum):
    """Vehicle ownership models."""
    TRADITIONAL = auto()       # Direct ownership
    LEASING = auto()           # Traditional leasing
    SUBSCRIPTION = auto()      # Flexible subscription
    USAGE_BASED = auto()       # Pay-per-use
    MOBILITY_AS_A_SERVICE = auto()  # Bundled mobility

class Region(Enum):
    """Geographic regions with different adoption patterns."""
    NORTH_AMERICA = auto()
    EUROPE = auto()
    CHINA = auto()
    JAPAN_KOREA = auto()
    EMERGING_MARKETS = auto()

class VehicleSegment(Enum):
    """Vehicle segments with different mobility characteristics."""
    CITY_CAR = auto()
    COMPACT = auto()
    MIDSIZE = auto()
    PREMIUM = auto()
    LUXURY = auto()
    COMMERCIAL_LIGHT = auto()
    COMMERCIAL_HEAVY = auto()

@dataclass
class MobilityService:
    """Represents a mobility service with its characteristics."""
    service_type: MobilityServiceType
    base_adoption: float  # Base adoption rate (0-1)
    growth_rate: float    # Annual growth rate
    peak_year: int        # Year of peak adoption
    region_factors: Dict[Region, float]  # Regional adoption factors
    segment_factors: Dict[VehicleSegment, float]  # Segment adoption factors

# --- Core Simulation Class ---

class NewMobilitySimulator:
    """Simulates the evolution of new mobility services and business models."""
    
    def __init__(self):
        # Initialize mobility services with base parameters
        self.services = {
            MobilityServiceType.RIDE_HAILING: MobilityService(
                service_type=MobilityServiceType.RIDE_HAILING,
                base_adoption=0.15,
                growth_rate=0.12,
                peak_year=2030,
                region_factors={
                    Region.NORTH_AMERICA: 1.0,
                    Region.EUROPE: 0.9,
                    Region.CHINA: 1.2,
                    Region.JAPAN_KOREA: 0.8,
                    Region.EMERGING_MARKETS: 0.7
                },
                segment_factors={
                    VehicleSegment.CITY_CAR: 1.2,
                    VehicleSegment.COMPACT: 1.1,
                    VehicleSegment.MIDSIZE: 1.0,
                    VehicleSegment.PREMIUM: 0.9,
                    VehicleSegment.LUXURY: 0.8,
                    VehicleSegment.COMMERCIAL_LIGHT: 0.5,
                    VehicleSegment.COMMERCIAL_HEAVY: 0.3
                }
            ),
            MobilityServiceType.CAR_SHARING: MobilityService(
                service_type=MobilityServiceType.CAR_SHARING,
                base_adoption=0.08,
                growth_rate=0.15,
                peak_year=2032,
                region_factors={
                    Region.NORTH_AMERICA: 0.9,
                    Region.EUROPE: 1.2,
                    Region.CHINA: 0.8,
                    Region.JAPAN_KOREA: 0.7,
                    Region.EMERGING_MARKETS: 0.6
                },
                segment_factors={
                    VehicleSegment.CITY_CAR: 1.3,
                    VehicleSegment.COMPACT: 1.1,
                    VehicleSegment.MIDSIZE: 0.9,
                    VehicleSegment.PREMIUM: 0.7,
                    VehicleSegment.LUXURY: 0.5,
                    VehicleSegment.COMMERCIAL_LIGHT: 0.8,
                    VehicleSegment.COMMERCIAL_HEAVY: 0.4
                }
            ),
            MobilityServiceType.ROBOTAXI: MobilityService(
                service_type=MobilityServiceType.ROBOTAXI,
                base_adoption=0.02,
                growth_rate=0.25,
                peak_year=2035,
                region_factors={
                    Region.NORTH_AMERICA: 1.1,
                    Region.EUROPE: 1.0,
                    Region.CHINA: 1.3,
                    Region.JAPAN_KOREA: 0.9,
                    Region.EMERGING_MARKETS: 0.5
                },
                segment_factors={
                    VehicleSegment.CITY_CAR: 1.4,
                    VehicleSegment.COMPACT: 1.2,
                    VehicleSegment.MIDSIZE: 1.0,
                    VehicleSegment.PREMIUM: 0.6,
                    VehicleSegment.LUXURY: 0.4,
                    VehicleSegment.COMMERCIAL_LIGHT: 0.3,
                    VehicleSegment.COMMERCIAL_HEAVY: 0.2
                }
            ),
            MobilityServiceType.SUBSCRIPTION: MobilityService(
                service_type=MobilityServiceType.SUBSCRIPTION,
                base_adoption=0.05,
                growth_rate=0.18,
                peak_year=2033,
                region_factors={
                    Region.NORTH_AMERICA: 1.0,
                    Region.EUROPE: 0.9,
                    Region.CHINA: 1.1,
                    Region.JAPAN_KOREA: 0.7,
                    Region.EMERGING_MARKETS: 0.4
                },
                segment_factors={
                    VehicleSegment.CITY_CAR: 0.8,
                    VehicleSegment.COMPACT: 1.0,
                    VehicleSegment.MIDSIZE: 1.2,
                    VehicleSegment.PREMIUM: 1.3,
                    VehicleSegment.LUXURY: 1.1,
                    VehicleSegment.COMMERCIAL_LIGHT: 0.9,
                    VehicleSegment.COMMERCIAL_HEAVY: 0.7
                }
            )
        }
        
        # Ownership model transition parameters
        self.ownership_params = {
            OwnershipModel.TRADITIONAL: {
                'decline_rate': 0.03,  # Annual decline rate
                'base_share': 0.8,     # Starting market share
                'region_variation': {
                    Region.NORTH_AMERICA: 1.0,
                    Region.EUROPE: 0.9,
                    Region.CHINA: 0.8,
                    Region.JAPAN_KOREA: 0.7,
                    Region.EMERGING_MARKETS: 0.6
                }
            },
            OwnershipModel.LEASING: {
                'base_share': 0.15,
                'growth_rate': 0.01,
                'peak_year': 2030,
                'decline_after_peak': 0.02
            },
            OwnershipModel.SUBSCRIPTION: {
                'base_share': 0.03,
                'growth_rate': 0.25,
                'saturation_share': 0.15,
                'saturation_year': 2035
            },
            OwnershipModel.USAGE_BASED: {
                'base_share': 0.01,
                'growth_rate': 0.3,
                'saturation_share': 0.1,
                'saturation_year': 2038
            },
            OwnershipModel.MOBILITY_AS_A_SERVICE: {
                'base_share': 0.01,
                'growth_rate': 0.35,
                'saturation_share': 0.2,
                'saturation_year': 2040
            }
        }
        
        # Revenue per kilometer by service type (USD/km)
        self.revenue_rates = {
            MobilityServiceType.RIDE_HAILING: 0.50,
            MobilityServiceType.CAR_SHARING: 0.30,
            MobilityServiceType.ROBOTAXI: 0.40,
            MobilityServiceType.SUBSCRIPTION: 0.25
        }
        
        # Cost per kilometer by service type (USD/km)
        self.cost_rates = {
            MobilityServiceType.RIDE_HAILING: 0.35,
            MobilityServiceType.CAR_SHARING: 0.20,
            MobilityServiceType.ROBOTAXI: 0.15,  # Lower due to autonomy
            MobilityServiceType.SUBSCRIPTION: 0.30
        }
    
    def simulate_service_adoption(
        self,
        years: np.ndarray,
        service_type: MobilityServiceType,
        region: Region,
        vehicle_segment: VehicleSegment
    ) -> np.ndarray:
        """Simulate adoption of a specific mobility service."""
        service = self.services[service_type]
        
        # Base adoption curve (logistic growth)
        x = (years - 2020) * service.growth_rate
        peak_offset = service.peak_year - 2020
        adoption = 1 / (1 + np.exp(-x + peak_offset/2))
        
        # Apply region and segment factors
        region_factor = service.region_factors.get(region, 1.0)
        segment_factor = service.segment_factors.get(vehicle_segment, 1.0)
        
        # Calculate final adoption rates
        adoption = adoption * service.base_adoption * region_factor * segment_factor
        
        # Add some noise
        noise = np.random.normal(0, 0.01, len(years))
        return np.clip(adoption + noise, 0, 1)
    
    def simulate_ownership_evolution(
        self,
        years: np.ndarray,
        region: Region,
        vehicle_segment: VehicleSegment
    ) -> Dict[OwnershipModel, np.ndarray]:
        """Simulate the evolution of ownership models."""
        results = {}
        
        # Traditional ownership
        trad = self.ownership_params[OwnershipModel.TRADITIONAL]
        region_factor = trad['region_variation'].get(region, 1.0)
        trad_share = trad['base_share'] * (1 - trad['decline_rate']) ** (years - 2020)
        trad_share = trad_share * region_factor
        results[OwnershipModel.TRADITIONAL] = trad_share
        
        # Leasing
        lease = self.ownership_params[OwnershipModel.LEASING]
        lease_share = np.minimum(
            lease['base_share'] * (1 + lease['growth_rate']) ** (years - 2020),
            lease['base_share'] * 1.5  # Cap at 1.5x base
        )
        # Apply decline after peak
        decline_mask = years > lease['peak_year']
        if np.any(decline_mask):
            decline_years = years[decline_mask] - lease['peak_year']
            lease_share[decline_mask] *= (1 - lease['decline_after_peak']) ** decline_years
        results[OwnershipModel.LEASING] = lease_share
        
        # Subscription
        sub = self.ownership_params[OwnershipModel.SUBSCRIPTION]
        sub_share = sub['saturation_share'] * (
            1 / (1 + np.exp(-sub['growth_rate'] * (years - (sub['saturation_year'] - 2020) / 2)))
        )
        results[OwnershipModel.SUBSCRIPTION] = sub_share
        
        # Usage-based
        usage = self.ownership_params[OwnershipModel.USAGE_BASED]
        usage_share = usage['saturation_share'] * (
            1 / (1 + np.exp(-usage['growth_rate'] * (years - (usage['saturation_year'] - 2020) / 2)))
        )
        results[OwnershipModel.USAGE_BASED] = usage_share
        
        # MaaS
        maas = self.ownership_params[OwnershipModel.MOBILITY_AS_A_SERVICE]
        maas_share = maas['saturation_share'] * (
            1 / (1 + np.exp(-maas['growth_rate'] * (years - (maas['saturation_year'] - 2020) / 2)))
        )
        results[OwnershipModel.MOBILITY_AS_A_SERVICE] = maas_share
        
        # Normalize to ensure total = 1
        total = sum(results.values())
        for model in results:
            results[model] = results[model] / total
        
        return results
    
    def calculate_service_economics(
        self,
        years: np.ndarray,
        service_type: MobilityServiceType,
        adoption_rates: np.ndarray,
        annual_km: float = 15000  # Average annual kilometers per vehicle
    ) -> Dict[str, np.ndarray]:
        """Calculate revenue and profit for a mobility service."""
        # Calculate vehicles in service (assuming total fleet size of 1M for scaling)
        vehicles = adoption_rates * 1_000_000
        
        # Calculate annual revenue and cost
        revenue_per_vehicle = self.revenue_rates[service_type] * annual_km
        cost_per_vehicle = self.cost_rates[service_type] * annual_km
        
        total_revenue = vehicles * revenue_per_vehicle / 1_000_000  # In millions
        total_cost = vehicles * cost_per_vehicle / 1_000_000
        profit = total_revenue - total_cost
        
        return {
            'vehicles': vehicles,
            'revenue_millions': total_revenue,
            'cost_millions': total_cost,
            'profit_millions': profit,
            'margin': np.divide(
                profit, 
                total_revenue, 
                out=np.zeros_like(profit), 
                where=total_revenue!=0
            )
        }

def run_new_mobility_simulation(
    start_year: int = 2020,
    end_year: int = 2040,
    regions: Optional[Union[List[Union[str, Region]], str]] = None,
    segments: Optional[Union[List[Union[str, VehicleSegment]], str]] = None,
    output_dir: Optional[Union[str, Path]] = None,
    save_results: bool = True
) -> Dict:
    """Run the new mobility simulation.
    
    Args:
        start_year: Start year of the simulation (default: 2020)
        end_year: End year of the simulation (default: 2040)
        regions: List of regions (as strings or Region enums) or 'all' for all regions
        segments: List of vehicle segments (as strings or VehicleSegment enums) or 'all' for all segments
        output_dir: Directory to save results (default: 'data/processed_data/new_mobility')
        save_results: Whether to save results to disk (default: True)
        
    Returns:
        Dictionary containing simulation results with service adoption, ownership models, and economic metrics
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
        segment_enums = list(VehicleSegment)
    else:
        segment_enums = []
        for s in segments if isinstance(segments, list) else [segments]:
            if isinstance(s, str):
                try:
                    segment_enums.append(VehicleSegment[s.upper()])
                except KeyError:
                    raise ValueError(f"Invalid segment: {s}. Valid segments are: {[e.name for e in VehicleSegment]}")
            else:
                segment_enums.append(s)
                
    # Convert regions and segments back to lists if they were passed as single values
    regions = region_enums
    segments = segment_enums

    years = np.arange(start_year, end_year + 1)
    simulator = NewMobilitySimulator()
    
    # Prepare results structure
    results = {
        'service_adoption': {},
        'ownership': {},
        'economics': {}
    }
    
    # Simulate service adoption
    for region in regions:
        region_key = region.name.lower()
        results['service_adoption'][region_key] = {}
        results['ownership'][region_key] = {}
        results['economics'][region_key] = {}
        
        for segment in segments:
            segment_key = segment.name.lower()
            results['service_adoption'][region_key][segment_key] = {}
            results['ownership'][region_key][segment_key] = {}
            results['economics'][region_key][segment_key] = {}
            
            # Simulate service adoption
            for service_type in simulator.services.keys():
                adoption = simulator.simulate_service_adoption(
                    years, service_type, region, segment
                )
                results['service_adoption'][region_key][segment_key][service_type.name] = adoption
                
                # Calculate economics for this service
                economics = simulator.calculate_service_economics(
                    years, service_type, adoption
                )
                results['economics'][region_key][segment_key][service_type.name] = economics
            
            # Simulate ownership evolution
            ownership = simulator.simulate_ownership_evolution(years, region, segment)
            results['ownership'][region_key][segment_key] = {
                model.name: share for model, share in ownership.items()
            }
    
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to get to the project root
    project_root = os.path.dirname(os.path.dirname(current_dir))
    # Define the output directory
    output_dir = os.path.join(project_root, 'data', 'processed_data', 'new_mobility')
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save service adoption data
    service_data = []
    for region_key, region_data in results['service_adoption'].items():
        for segment_key, segment_data in region_data.items():
            for service_key, adoption in segment_data.items():
                for year, rate in zip(years, adoption):
                    service_data.append({
                        'year': year,
                        'region': region_key,
                        'segment': segment_key,
                        'service': service_key,
                        'adoption_rate': rate
                    })
    
    service_file = os.path.join(output_dir, 'service_adoption.csv')
    pd.DataFrame(service_data).to_csv(service_file, index=False)
    print(f"Saved service adoption data to: {service_file}")
    
    # Save ownership data
    ownership_data = []
    for region_key, region_data in results['ownership'].items():
        for segment_key, segment_data in region_data.items():
            for model_key, shares in segment_data.items():
                for year, share in zip(years, shares):
                    ownership_data.append({
                        'year': year,
                        'region': region_key,
                        'segment': segment_key,
                        'ownership_model': model_key,
                        'market_share': share
                    })
    
    ownership_file = os.path.join(output_dir, 'ownership_models.csv')
    pd.DataFrame(ownership_data).to_csv(ownership_file, index=False)
    print(f"Saved ownership data to: {ownership_file}")
    
    # Save economic data
    economic_data = []
    for region_key, region_data in results['economics'].items():
        for segment_key, segment_data in region_data.items():
            for service_key, metrics in segment_data.items():
                for year, (veh, rev, cost, prof, marg) in enumerate(zip(
                    metrics['vehicles'],
                    metrics['revenue_millions'],
                    metrics['cost_millions'],
                    metrics['profit_millions'],
                    metrics['margin']
                ), start=start_year):
                    economic_data.append({
                        'year': year,
                        'region': region_key,
                        'segment': segment_key,
                        'service': service_key,
                        'vehicles': veh,
                        'revenue_millions': rev,
                        'cost_millions': cost,
                        'profit_millions': prof,
                        'margin': marg
                    })
    
    economics_file = os.path.join(output_dir, 'economic_metrics.csv')
    pd.DataFrame(economic_data).to_csv(economics_file, index=False)
    print(f"Saved economic data to: {economics_file}")
    
    return results

def plot_new_mobility_results(results: Dict, save_path: str = None):
    """Plot the new mobility simulation results."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(16, 12))
        
        # Prepare data for plotting
        years = np.arange(2020, 2041)
        
        # Plot 1: Service Adoption by Region (average across segments)
        plt.subplot(2, 2, 1)
        for region in results['service_adoption'].keys():
            # Average adoption across segments for this region
            avg_adoption = np.zeros_like(years, dtype=float)
            count = 0
            
            for segment in results['service_adoption'][region].values():
                for service in segment.values():
                    avg_adoption += service
                    count += 1
            
            if count > 0:
                avg_adoption /= count
                plt.plot(years, avg_adoption * 100, label=region.replace('_', ' ').title())
        
        plt.title('Average Mobility Service Adoption by Region')
        plt.xlabel('Year')
        plt.ylabel('Adoption Rate (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Ownership Model Evolution
        plt.subplot(2, 2, 2)
        ownership_data = {
            model.name: [] for model in OwnershipModel
        }
        
        # Get data for North America, Midsize segment as example
        region_key = 'north_america'
        segment_key = 'midsize'
        
        for model, shares in results['ownership'][region_key][segment_key].items():
            plt.plot(years, np.array(shares) * 100, label=model.replace('_', ' ').title())
        
        plt.title(f'Ownership Model Evolution\n({region_key.replace("_", " ").title()}, {segment_key.replace("_", " ").title()})')
        plt.xlabel('Year')
        plt.ylabel('Market Share (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 3: Service Economics (Profitability)
        plt.subplot(2, 2, 3)
        # Get data for Robotaxi service across regions
        service_key = 'ROBOTAXI'
        segment_key = 'midsize'
        
        for region in results['economics'].keys():
            if segment_key in results['economics'][region]:
                if service_key in results['economics'][region][segment_key]:
                    margins = results['economics'][region][segment_key][service_key]['margin'] * 100
                    plt.plot(years, margins, label=region.replace('_', ' ').title())
        
        plt.title(f'{service_key.replace("_", " ").title()} Profit Margins by Region')
        plt.xlabel('Year')
        plt.ylabel('Profit Margin (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 4: Service Mix Evolution
        plt.subplot(2, 2, 4)
        # Get data for North America, Midsize segment
        region_key = 'north_america'
        segment_key = 'midsize'
        
        for service, adoption in results['service_adoption'][region_key][segment_key].items():
            plt.plot(years, adoption * 100, label=service.replace('_', ' ').title())
        
        plt.title(f'Service Mix Evolution\n({region_key.replace("_", " ").title()}, {segment_key.replace("_", " ").title()})')
        plt.xlabel('Year')
        plt.ylabel('Adoption Rate (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {os.path.abspath(save_path)}")
        
        plt.show()
        
    except ImportError as e:
        print(f"Error generating plots: {e}")
        print("Required packages: matplotlib, seaborn")

if __name__ == '__main__':
    print("Running New Mobility & Business Model Evolution Simulation (2020-2040)...")
    
    # Run the simulation
    results = run_new_mobility_simulation(2020, 2040)
    
    # Plot the results
    plot_new_mobility_results(
        results,
        save_path='../../reports/figures/new_mobility_evolution.png'
    )
    
    print("\n=== Simulation Complete ===")
    print("Output files saved to data/processed_data/new_mobility/")
    print("Visualization saved to reports/figures/new_mobility_evolution.png")
