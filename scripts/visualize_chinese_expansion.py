"""
Visualization script for Chinese Manufacturer Expansion simulation results.

This script generates visualizations for the Chinese vehicle manufacturer global expansion simulation.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

# Set up visualization style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed_data" / "chinese_expansion"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures" / "chinese_expansion"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data() -> Dict[str, pd.DataFrame]:
    """Load simulation results from CSV files."""
    data = {}
    for file in DATA_DIR.glob("*.csv"):
        name = file.stem
        try:
            df = pd.read_csv(file)
            if not df.empty:
                data[name] = df
                print(f"Loaded {file.name} with {len(df)} rows")
            else:
                print(f"Warning: {file.name} is empty")
        except Exception as e:
            print(f"Error loading {file.name}: {str(e)}")
    
    if not data:
        print(f"No data files found in {DATA_DIR}")
    return data

def plot_market_share_by_region(data: pd.DataFrame, output_dir: Path):
    """Plot market share by region over time."""
    plt.figure(figsize=(14, 8))
    
    # Pivot data for plotting
    pivot_data = data.pivot_table(
        index='year',
        columns='region',
        values='market_share',
        aggfunc='sum'
    )
    
    # Plot
    ax = pivot_data.plot(marker='o')
    plt.title('Chinese OEM Market Share by Region (2025-2040)')
    plt.xlabel('Year')
    plt.ylabel('Market Share (%)')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the figure
    output_path = output_dir / 'market_share_by_region.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved market share by region plot to: {output_path}")

def plot_market_share_by_segment(data: pd.DataFrame, output_dir: Path):
    """Plot market share by vehicle segment over time."""
    plt.figure(figsize=(14, 8))
    
    # Pivot data for plotting
    pivot_data = data.pivot_table(
        index='year',
        columns='segment',
        values='market_share',
        aggfunc='mean'
    )
    
    # Plot
    ax = pivot_data.plot(marker='o')
    plt.title('Chinese OEM Market Share by Vehicle Segment (2025-2040)')
    plt.xlabel('Year')
    plt.ylabel('Market Share (%)')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the figure
    output_path = output_dir / 'market_share_by_segment.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved market share by segment plot to: {output_path}")

def plot_revenue_growth(data: pd.DataFrame, output_dir: Path):
    """Plot revenue growth by region."""
    plt.figure(figsize=(14, 8))
    
    # Pivot data for plotting
    pivot_data = data.pivot_table(
        index='year',
        columns='region',
        values='revenue_millions',
        aggfunc='sum'
    )
    
    # Plot
    ax = pivot_data.plot(marker='o')
    plt.title('Chinese OEM Revenue by Region (2025-2040)')
    plt.xlabel('Year')
    plt.ylabel('Revenue (Millions USD)')
    plt.grid(True, alpha=0.3)
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the figure
    output_path = output_dir / 'revenue_growth.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved revenue growth plot to: {output_path}")

def plot_strategy_distribution(data: pd.DataFrame, output_dir: Path):
    """Plot distribution of expansion strategies over time."""
    # Count strategies by year
    strategy_counts = data.groupby(['year', 'strategy']).size().unstack().fillna(0)
    
    # Plot
    plt.figure(figsize=(14, 8))
    strategy_counts.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Distribution of Chinese OEM Expansion Strategies (2025-2040)')
    plt.xlabel('Year')
    plt.ylabel('Number of Market Entries')
    plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save the figure
    output_path = output_dir / 'strategy_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved strategy distribution plot to: {output_path}")

def main():
    """Main function to generate all visualizations."""
    print("Loading data...\n")
    
    # Load data
    try:
        data = load_data()
        if not data:
            print("No data files found. Please run the simulation first.")
            return
        
        # Get the main results dataframe
        if 'market_share_evolution' in data:
            df = data['market_share_evolution']
            
            # Generate plots
            print("\nGenerating visualizations...")
            plot_market_share_by_region(df, OUTPUT_DIR)
            plot_market_share_by_segment(df, OUTPUT_DIR)
            plot_revenue_growth(df, OUTPUT_DIR)
            plot_strategy_distribution(df, OUTPUT_DIR)
            
            print("\nAll visualizations have been generated!")
        else:
            print("Error: 'market_share_evolution' data not found in the results.")
            print("Available data keys:", list(data.keys()))
            
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
