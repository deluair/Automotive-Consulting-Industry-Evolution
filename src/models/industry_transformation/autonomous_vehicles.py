"""
Autonomous Vehicle & ADAS Evolution Simulation (2025-2040)

This module simulates the adoption of different levels of autonomous driving technology
across various vehicle segments, considering technology readiness, regulatory environment,
and consumer acceptance factors.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union

# --- Helper Functions ---

def logistic_growth(year: Union[int, np.ndarray], l_max: float, k: float, year_mid: float) -> Union[float, np.ndarray]:
    """
    Calculate logistic growth (S-curve) for technology adoption.
    
    Args:
        year: Year or array of years for simulation
        l_max: Maximum adoption level (0-1)
        k: Growth rate (steepness of the curve)
        year_mid: Year when adoption reaches 50% of l_max
        
    Returns:
        Adoption rate (0-1) for the given year(s)
    """
    try:
        return l_max / (1 + np.exp(-k * (year - year_mid)))
    except OverflowError:
        return np.where(-k * (year - year_mid) > 0, l_max, 0.0)

# --- Core Simulation Classes ---

class AutonomousVehicleAdoption:
    """Simulates adoption of autonomous vehicle technology by SAE level and vehicle segment."""
    
    # SAE Level definitions (0-5)
    SAE_LEVELS = {
        0: 'No Automation',
        1: 'Driver Assistance',
        2: 'Partial Automation',
        3: 'Conditional Automation',
        4: 'High Automation',
        5: 'Full Automation'
    }
    
    def __init__(self):
        # Default parameters for different autonomy levels
        # Format: {
        #   'segment': {
        #       'l_max': max penetration (0-1),
        #       'k': growth rate,
        #       'year_mid': midpoint year,
        #       'min_year': earliest year available
        #   }
        # }
        self.parameters = {
            # Luxury/ Premium vehicles (earlier, higher adoption)
            'luxury': {
                1: {'l_max': 0.98, 'k': 0.8, 'year_mid': 2023, 'min_year': 2020},  # L1: Common today
                2: {'l_max': 0.95, 'k': 0.7, 'year_mid': 2024, 'min_year': 2020},  # L2: Common in premium
                3: {'l_max': 0.70, 'k': 0.6, 'year_mid': 2028, 'min_year': 2023},  # L3: Conditional automation
                4: {'l_max': 0.50, 'k': 0.5, 'year_mid': 2032, 'min_year': 2026},  # L4: High automation
                5: {'l_max': 0.25, 'k': 0.4, 'year_mid': 2035, 'min_year': 2030}   # L5: Full automation
            },
            # Mass market passenger vehicles
            'mass_market': {
                1: {'l_max': 0.95, 'k': 0.7, 'year_mid': 2024, 'min_year': 2020},
                2: {'l_max': 0.90, 'k': 0.6, 'year_mid': 2026, 'min_year': 2020},
                3: {'l_max': 0.60, 'k': 0.5, 'year_mid': 2030, 'min_year': 2025},
                4: {'l_max': 0.40, 'k': 0.4, 'year_mid': 2034, 'min_year': 2028},
                5: {'l_max': 0.15, 'k': 0.3, 'year_mid': 2038, 'min_year': 2032}
            },
            # Commercial vehicles (trucks)
            'commercial': {
                1: {'l_max': 0.90, 'k': 0.6, 'year_mid': 2025, 'min_year': 2020},
                2: {'l_max': 0.85, 'k': 0.5, 'year_mid': 2027, 'min_year': 2020},
                3: {'l_max': 0.70, 'k': 0.5, 'year_mid': 2029, 'min_year': 2024},  # Higher L3 for highway platooning
                4: {'l_max': 0.60, 'k': 0.5, 'year_mid': 2032, 'min_year': 2027},  # Strong business case for L4
                5: {'l_max': 0.10, 'k': 0.3, 'year_mid': 2040, 'min_year': 2035}   # Limited L5 use cases
            },
            # Robotaxis/ Mobility as a Service
            'robotaxi': {
                1: {'l_max': 0.95, 'k': 0.8, 'year_mid': 2024, 'min_year': 2020},
                2: {'l_max': 0.90, 'k': 0.7, 'year_mid': 2025, 'min_year': 2020},
                3: {'l_max': 0.80, 'k': 0.7, 'year_mid': 2027, 'min_year': 2023},  # Rapid L3 adoption
                4: {'l_max': 0.90, 'k': 0.6, 'year_mid': 2030, 'min_year': 2025},  # Strong L4 focus
                5: {'l_max': 0.40, 'k': 0.4, 'year_mid': 2035, 'min_year': 2030}   # Some L5 in controlled areas
            }
        }
    
    def simulate_segment(self, years: np.ndarray, segment: str) -> pd.DataFrame:
        """
        Simulate adoption of all autonomy levels for a vehicle segment.
        
        Args:
            years: Array of years to simulate
            segment: Vehicle segment ('luxury', 'mass_market', 'commercial', 'robotaxi')
            
        Returns:
            DataFrame with adoption rates by autonomy level and year
        """
        if segment not in self.parameters:
            raise ValueError(f"Unknown segment: {segment}. Choose from {list(self.parameters.keys())}")
        
        results = {'Year': years}
        
        for level in range(1, 6):  # SAE Levels 1-5
            params = self.parameters[segment][level]
            # Calculate adoption curve
            adoption = logistic_growth(years, params['l_max'], params['k'], params['year_mid'])
            # Apply minimum year constraint
            adoption[years < params['min_year']] = 0
            # Ensure we don't exceed 100% for any level
            results[f'L{level}'] = np.minimum(adoption, 1.0)
        
        return pd.DataFrame(results)
    
    def calculate_cumulative_adoption(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate cumulative adoption across autonomy levels.
        Assumes higher levels include lower levels' capabilities.
        """
        result = df.copy()
        # L1 is the base level
        result['L1_cumulative'] = result['L1']
        
        # Higher levels include all lower levels
        for level in range(2, 6):
            result[f'L{level}_cumulative'] = result[f'L{level}'] + result[f'L{level-1}_cumulative']
            # Cap at 100%
            result[f'L{level}_cumulative'] = np.minimum(result[f'L{level}_cumulative'], 1.0)
        
        return result

def run_av_simulation(start_year: int = 2020, end_year: int = 2040) -> Dict[str, pd.DataFrame]:
    """
    Run the autonomous vehicle adoption simulation for all segments.
    
    Args:
        start_year: First year of simulation
        end_year: Last year of simulation
        
    Returns:
        Dictionary of DataFrames with results for each segment
    """
    years = np.arange(start_year, end_year + 1)
    av = AutonomousVehicleAdoption()
    
    results = {}
    
    # Simulate for each segment
    for segment in av.parameters.keys():
        # Get base adoption
        df = av.simulate_segment(years, segment)
        # Calculate cumulative adoption
        df = av.calculate_cumulative_adoption(df)
        results[segment] = df
        
        # Save to CSV
        import os
        os.makedirs('../../data/processed_data', exist_ok=True)
        df.to_csv(f'../../data/processed_data/av_adoption_{segment}.csv', index=False)
    
    # Create combined DataFrame with key metrics
    combined_data = []
    for segment, df in results.items():
        for _, row in df.iterrows():
            combined_data.append({
                'Year': row['Year'],
                'Segment': segment,
                'L2+_Penetration': row.get('L2_cumulative', 0) * 100,  # % of vehicles with L2 or higher
                'L3+_Penetration': row.get('L3_cumulative', 0) * 100,  # % of vehicles with L3 or higher
                'L4+_Penetration': row.get('L4_cumulative', 0) * 100   # % of vehicles with L4 or higher
            })
    
    combined_df = pd.DataFrame(combined_data)
    combined_df.to_csv('../../data/processed_data/av_adoption_combined.csv', index=False)
    
    return results

def plot_av_adoption(results: Dict[str, pd.DataFrame], save_path: str = None):
    """
    Plot autonomous vehicle adoption curves.
    
    Args:
        results: Dictionary of DataFrames from run_av_simulation()
        save_path: Optional path to save the figure
    """
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        sns.set_theme(style="whitegrid")
        
        # Create a 2x2 grid of plots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Autonomous Vehicle Adoption by Segment (2020-2040)', fontsize=16)
        
        # Plot each segment
        for idx, (segment, df) in enumerate(results.items()):
            ax = axes[idx//2, idx%2]
            
            # Plot each autonomy level
            for level in range(1, 6):
                ax.plot(df['Year'], df[f'L{level}']*100, 
                       label=f'L{level} ({AutonomousVehicleAdoption.SAE_LEVELS[level][0]}' + 
                             f'{AutonomousVehicleAdoption.SAE_LEVELS[level][1:].lower()})')
            
            ax.set_title(segment.replace('_', ' ').title())
            ax.set_xlabel('Year')
            ax.set_ylabel('Penetration (%)')
            ax.set_ylim(0, 105)
            ax.legend(loc='upper left')
            ax.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            import os
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {os.path.abspath(save_path)}")
        
        plt.show()
        
    except ImportError:
        print("Error: matplotlib and seaborn are required for plotting.")
        print("Install with: pip install matplotlib seaborn")

if __name__ == '__main__':
    print("Running Autonomous Vehicle Adoption Simulation (2020-2040)...")
    
    # Run the simulation
    results = run_av_simulation(2020, 2040)
    
    # Plot the results
    plot_av_adoption(
        results,
        save_path='../../reports/figures/av_adoption_curves.png'
    )
    
    # Print key metrics
    print("\n=== Key Metrics ===")
    for segment, df in results.items():
        print(f"\n--- {segment.replace('_', ' ').title()} ---")
        for year in [2025, 2030, 2035, 2040]:
            row = df[df['Year'] == year].iloc[0] if year in df['Year'].values else None
            if row is not None:
                print(f"{year} - L2+: {row.get('L2_cumulative', 0)*100:.1f}%, "
                      f"L3+: {row.get('L3_cumulative', 0)*100:.1f}%, "
                      f"L4+: {row.get('L4_cumulative', 0)*100:.1f}%")
    
    print("\nSimulation completed successfully!")
