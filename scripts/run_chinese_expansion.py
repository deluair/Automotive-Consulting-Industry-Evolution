"""
Script to run the Chinese manufacturer expansion simulation and generate visualizations.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional, Union

# Add both project root and src directories to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from models.industry_reconfiguration.chinese_manufacturer_expansion import (
    run_chinese_expansion_simulation,
    Region,
    MarketSegment
)

def main():
    """Run the Chinese manufacturer expansion simulation and generate visualizations."""
    print("Running Chinese Manufacturer Expansion Simulation (2025-2040)...")
    
    # Run the simulation
    results = run_chinese_expansion_simulation(
        start_year=2025,
        end_year=2040,
        regions=[
            Region.NORTH_AMERICA,
            Region.EUROPE,
            Region.CHINA,
            Region.EMERGING_MARKETS
        ],
        segments=[
            MarketSegment.ENTRY,
            MarketSegment.MASS_MARKET,
            MarketSegment.PREMIUM,
            MarketSegment.LUXURY,
            MarketSegment.COMMERCIAL,
            MarketSegment.EV
        ]
    )
    
    print("\nSimulation completed successfully!")
    print("\nGenerating visualizations...")
    
    # Import and run the visualization script
    from scripts.visualize_chinese_expansion import main as generate_visualizations
    generate_visualizations()
    
    print("\nAll tasks completed!")

if __name__ == "__main__":
    main()
