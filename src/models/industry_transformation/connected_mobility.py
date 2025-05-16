"""
Connected Mobility & Software-Defined Vehicle Transition (2025-2040)

This module simulates the evolution of connected car technologies, software platforms,
and the transition to software-defined vehicles across different vehicle segments.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union
import os

# --- Helper Functions ---

def logistic_growth(year: Union[int, np.ndarray], l_max: float, k: float, year_mid: float) -> Union[float, np.ndarray]:
    """Calculate logistic growth (S-curve) for technology adoption."""
    try:
        return l_max / (1 + np.exp(-k * (year - year_mid)))
    except OverflowError:
        return np.where(-k * (year - year_mid) > 0, l_max, 0.0)

# --- Core Simulation Classes ---

class ConnectedMobilitySimulator:
    """Simulates the evolution of connected mobility and software-defined vehicles."""
    
    def __init__(self):
        # Connectivity technology parameters
        self.connectivity_tech = {
            '4G': {'peak_year': 2025, 'decline_start': 2028, 'k': 0.5},
            '5G': {'adoption_start': 2022, 'peak_year': 2030, 'decline_start': 2035, 'k': 0.6},
            '5G_Advanced': {'adoption_start': 2025, 'peak_year': 2035, 'k': 0.5},
            '6G': {'adoption_start': 2030, 'peak_year': 2040, 'k': 0.4}
        }
        
        # V2X communication types
        self.v2x_types = {
            'V2V': {'max_penetration': 0.85, 'k': 0.5, 'mid_year': 2028},
            'V2I': {'max_penetration': 0.75, 'k': 0.4, 'mid_year': 2029},
            'V2P': {'max_penetration': 0.65, 'k': 0.4, 'mid_year': 2030},
            'V2N': {'max_penetration': 0.95, 'k': 0.6, 'mid_year': 2027},
            'V2G': {'max_penetration': 0.55, 'k': 0.3, 'mid_year': 2032}
        }
        
        # Software platform parameters by segment
        self.software_platforms = {
            'luxury': {
                'proprietary': 0.65,  # Base proportion using proprietary platforms
                'android_auto': 0.15,
                'qnx': 0.10,
                'linux_ag': 0.10
            },
            'mass_market': {
                'proprietary': 0.40,
                'android_auto': 0.35,
                'qnx': 0.15,
                'linux_ag': 0.10
            },
            'commercial': {
                'proprietary': 0.80,
                'android_auto': 0.10,
                'qnx': 0.05,
                'linux_ag': 0.05
            }
        }
        
        # Software development cost parameters (millions USD per year)
        self.software_costs = {
            'luxury': {'2025': 250, '2030': 350, '2035': 400, '2040': 450},
            'mass_market': {'2025': 150, '2030': 250, '2035': 300, '2040': 350},
            'commercial': {'2025': 100, '2030': 180, '2035': 250, '2040': 300}
        }
    
    def simulate_connectivity_evolution(self, years: np.ndarray) -> pd.DataFrame:
        """Simulate the evolution of connectivity technologies."""
        results = {'Year': years}
        
        # Simulate each technology's adoption
        for tech, params in self.connectivity_tech.items():
            if tech == '4G':
                # 4G is declining
                growth = logistic_growth(years, 1.0, 0.6, 2025)
                decline = 1 - logistic_growth(years, 1.0, 0.5, 2028)
                results[tech] = growth * decline
            else:
                # Newer technologies are growing
                if 'adoption_start' in params:
                    mask = years >= params['adoption_start']
                    tech_years = years[mask]
                    adoption = np.zeros_like(years, dtype=float)
                    adoption[mask] = logistic_growth(
                        tech_years, 
                        1.0, 
                        params['k'], 
                        params['peak_year']
                    )
                    results[tech] = adoption
                else:
                    results[tech] = 0.0
        
        return pd.DataFrame(results)
    
    def simulate_v2x_adoption(self, years: np.ndarray) -> pd.DataFrame:
        """Simulate V2X technology adoption."""
        results = {'Year': years}
        
        for v2x_type, params in self.v2x_types.items():
            results[v2x_type] = logistic_growth(
                years,
                params['max_penetration'],
                params['k'],
                params['mid_year']
            )
        
        return pd.DataFrame(results)
    
    def simulate_software_platforms(self, years: np.ndarray) -> Dict[str, pd.DataFrame]:
        """Simulate software platform evolution by segment."""
        results = {}
        
        for segment, platforms in self.software_platforms.items():
            df = pd.DataFrame({'Year': years})
            
            # Base platform shares
            for platform, share in platforms.items():
                if platform == 'proprietary':
                    # Proprietary share decreases over time
                    df[platform] = share * (1 - logistic_growth(years, 0.8, 0.4, 2030))
                else:
                    # Other platforms grow
                    growth = logistic_growth(years, 1.0, 0.5, 2030)
                    df[platform] = share * growth
            
            # Ensure total doesn't exceed 100%
            total = sum(df[col].sum() for col in df.columns if col != 'Year')
            if total > 0:
                for col in df.columns:
                    if col != 'Year':
                        df[col] = df[col] / total
            
            results[segment] = df
        
        return results
    
    def simulate_software_costs(self, years: np.ndarray) -> Dict[str, pd.DataFrame]:
        """Simulate software development costs by segment."""
        results = {}
        
        for segment, costs in self.software_costs.items():
            # Create a DataFrame with the known years
            known_years = np.array([int(y) for y in costs.keys()])
            known_values = np.array([costs[y] for y in costs.keys()])
            
            # Interpolate for all years
            all_years = np.array(years)
            interp_values = np.interp(all_years, known_years, known_values)
            
            # Add some noise to make it more realistic
            noise = np.random.normal(0, 5, len(all_years))
            interp_values = np.maximum(10, interp_values + noise)  # Ensure no negative costs
            
            results[segment] = pd.DataFrame({
                'Year': years,
                'Software_Development_Cost_Millions': interp_values
            })
        
        return results

def run_connected_mobility_simulation(start_year: int = 2020, end_year: int = 2040) -> Dict[str, Union[pd.DataFrame, Dict]]:
    """Run the complete connected mobility simulation."""
    years = np.arange(start_year, end_year + 1)
    simulator = ConnectedMobilitySimulator()
    
    # Run all simulations
    connectivity = simulator.simulate_connectivity_evolution(years)
    v2x = simulator.simulate_v2x_adoption(years)
    software_platforms = simulator.simulate_software_platforms(years)
    software_costs = simulator.simulate_software_costs(years)
    
    # Save results
    os.makedirs('../../data/processed_data', exist_ok=True)
    
    # Save connectivity data
    connectivity.to_csv('../../data/processed_data/connectivity_evolution.csv', index=False)
    v2x.to_csv('../../data/processed_data/v2x_adoption.csv', index=False)
    
    # Save platform data by segment
    for segment, df in software_platforms.items():
        df.to_csv(f'../../data/processed_data/software_platforms_{segment}.csv', index=False)
    
    # Save cost data by segment
    for segment, df in software_costs.items():
        df.to_csv(f'../../data/processed_data/software_costs_{segment}.csv', index=False)
    
    # Create a combined summary
    summary = {
        'connectivity': connectivity,
        'v2x': v2x,
        'software_platforms': software_platforms,
        'software_costs': software_costs
    }
    
    return summary

def plot_connected_mobility_results(results: Dict[str, Union[pd.DataFrame, Dict]], save_path: str = None):
    """Plot the connected mobility simulation results."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(16, 12))
        
        # Plot 1: Connectivity Technology Evolution
        plt.subplot(2, 2, 1)
        connectivity = results['connectivity']
        for col in connectivity.columns:
            if col != 'Year':
                plt.plot(connectivity['Year'], connectivity[col]*100, label=col, marker='o')
        plt.title('Connectivity Technology Evolution')
        plt.xlabel('Year')
        plt.ylabel('Market Share (%)')
        plt.legend()
        plt.grid(True)
        
        # Plot 2: V2X Adoption
        plt.subplot(2, 2, 2)
        v2x = results['v2x']
        for col in v2x.columns:
            if col != 'Year':
                plt.plot(v2x['Year'], v2x[col]*100, label=col, marker='s')
        plt.title('V2X Technology Adoption')
        plt.xlabel('Year')
        plt.ylabel('Penetration Rate (%)')
        plt.legend()
        plt.grid(True)
        
        # Plot 3: Software Platform Evolution (Luxury Segment)
        plt.subplot(2, 2, 3)
        platforms = results['software_platforms']['luxury']
        for col in platforms.columns:
            if col != 'Year':
                plt.plot(platforms['Year'], platforms[col]*100, label=col.replace('_', ' ').title(), marker='^')
        plt.title('Software Platform Evolution (Luxury Segment)')
        plt.xlabel('Year')
        plt.ylabel('Market Share (%)')
        plt.legend()
        plt.grid(True)
        
        # Plot 4: Software Development Costs
        plt.subplot(2, 2, 4)
        for segment, df in results['software_costs'].items():
            plt.plot(df['Year'], df['Software_Development_Cost_Millions'], 
                    label=segment.replace('_', ' ').title(), marker='*')
        plt.title('Annual Software Development Costs by Segment')
        plt.xlabel('Year')
        plt.ylabel('Cost (Millions USD)')
        plt.legend()
        plt.grid(True)
        
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
    print("Running Connected Mobility & SDV Simulation (2020-2040)...")
    
    # Run the simulation
    results = run_connected_mobility_simulation(2020, 2040)
    
    # Plot the results
    plot_connected_mobility_results(
        results,
        save_path='../../reports/figures/connected_mobility_evolution.png'
    )
    
    # Print key metrics
    print("\n=== Simulation Complete ===")
    print("Output files saved to data/processed_data/")
    print("Visualization saved to reports/figures/connected_mobility_evolution.png")
