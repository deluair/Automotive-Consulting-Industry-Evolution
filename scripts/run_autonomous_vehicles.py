"""
Autonomous Vehicle Adoption Simulation Runner

This script runs the autonomous vehicle adoption simulation and generates visualizations.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from models.industry_transformation.autonomous_vehicles import (
    run_av_simulation,
    plot_av_adoption
)
import pandas as pd
import os

# Ensure output directories exist
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed_data" / "autonomous_vehicles"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PLOT_DIR = PROJECT_ROOT / "reports" / "figures" / "autonomous_vehicles"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("Starting Autonomous Vehicle Adoption Simulation (2025-2040)...")
    
    # Run the simulation
    results = run_av_simulation(start_year=2025, end_year=2040)
    
    # Save results to CSV
    for segment, df in results.items():
        # Clean up segment name for filename
        filename = f"av_adoption_{segment.lower().replace(' ', '_')}.csv"
        filepath = OUTPUT_DIR / filename
        df.to_csv(filepath, index=False)
        print(f"Saved {segment} results to {filepath}")
    
    # Generate and save visualizations
    plot_path = PLOT_DIR / "av_adoption_curves.png"
    plot_av_adoption(results, save_path=str(plot_path))
    print(f"\nSaved adoption curves to {plot_path}")
    
    # Create a summary of adoption in 2030 and 2040
    summary_data = []
    for segment, df in results.items():
        for sae_level in range(6):  # SAE levels 0-5
            col = f'SAE {sae_level}'
            if col in df.columns:
                summary_data.append({
                    'Segment': segment,
                    'SAE Level': sae_level,
                    'Adoption 2030': df[df['Year'] == 2030][col].values[0],
                    'Adoption 2040': df[df['Year'] == 2040][col].values[0]
                })
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = OUTPUT_DIR / "av_adoption_summary.csv"
    summary_df.to_csv(summary_file, index=False)
    print(f"\nSaved adoption summary to {summary_file}")
    
    print("\nSimulation completed successfully!")

if __name__ == "__main__":
    main()
