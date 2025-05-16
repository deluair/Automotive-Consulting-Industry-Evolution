"""
Visualization script for New Mobility simulation results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional
import os

# Set the style
sns.set_theme(style="whitegrid")

def load_data(results_dir: str) -> Dict[str, pd.DataFrame]:
    """Load the simulation results from CSV files."""
    results_dir = Path(results_dir)
    
    return {
        'service_adoption': pd.read_csv(results_dir / 'service_adoption.csv'),
        'ownership': pd.read_csv(results_dir / 'ownership_models.csv'),
        'economics': pd.read_csv(results_dir / 'economic_metrics.csv')
    }

def plot_service_adoption(data: pd.DataFrame, output_dir: Path):
    """Plot service adoption over time by region and segment."""
    # Create a figure with subplots for each region and segment
    regions = data['region'].unique()
    segments = data['segment'].unique()
    services = data['service'].unique()
    
    for region in regions:
        plt.figure(figsize=(14, 8))
        
        # Filter data for the current region
        region_data = data[data['region'] == region]
        
        if region_data.empty:
            continue
            
        # Pivot to have services as columns
        pivot_data = region_data.pivot_table(
            index='year', 
            columns='service', 
            values='adoption_rate',
            aggfunc='mean'  # In case there are multiple entries per year
        )
        
        # Plot each service type
        sns.lineplot(data=pivot_data, markers=True, dashes=False)
        
        plt.title(f'Service Adoption in {region.title()}')
        plt.xlabel('Year')
        plt.ylabel('Adoption Rate')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        # Save the figure
        output_path = output_dir / f'service_adoption_{region.lower()}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved service adoption plot to: {output_path}")

def plot_ownership_evolution(data: pd.DataFrame, output_dir: Path):
    """Plot ownership model evolution over time by region and segment."""
    # Create a figure with subplots for each region and segment
    regions = data['region'].unique()
    segments = data['segment'].unique()
    
    for region in regions:
        plt.figure(figsize=(14, 8))
        
        # Filter data for the current region
        region_data = data[data['region'] == region]
        
        if region_data.empty:
            continue
            
        # Pivot to have ownership models as columns
        pivot_data = region_data.pivot_table(
            index='year', 
            columns='ownership_model', 
            values='market_share',
            aggfunc='mean'  # In case there are multiple entries per year
        )
        
        # Plot each ownership model
        sns.lineplot(data=pivot_data, markers=True, dashes=False)
        
        plt.title(f'Ownership Model Evolution in {region.title()}')
        plt.xlabel('Year')
        plt.ylabel('Market Share')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        # Save the figure
        output_path = output_dir / f'ownership_{region.lower()}.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved ownership plot to: {output_path}")

def plot_economic_metrics(data: pd.DataFrame, output_dir: Path):
    """Plot economic metrics over time by region and segment."""
    # Group by year, region, and segment to get aggregated metrics
    grouped = data.groupby(['year', 'region', 'segment', 'service']).agg({
        'revenue_millions': 'sum',
        'profit_millions': 'sum',
        'margin': 'mean'
    }).reset_index()
    
    # Plot revenue and profit for each region and segment
    regions = grouped['region'].unique()
    segments = grouped['segment'].unique()
    
    for region in regions:
        for segment in segments:
            # Filter data
            mask = (grouped['region'] == region) & (grouped['segment'] == segment)
            segment_data = grouped[mask]
            
            if segment_data.empty:
                continue
                
            # Create a figure with subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
            
            # Plot revenue and profit
            pivot_rev = segment_data.pivot(
                index='year',
                columns='service',
                values='revenue_millions'
            )
            pivot_rev.plot(ax=ax1, marker='o')
            ax1.set_title(f'Revenue by Service Type in {region.title()} - {segment.title()}')
            ax1.set_ylabel('Revenue (Millions USD)')
            
            # Plot profit
            pivot_profit = segment_data.pivot(
                index='year',
                columns='service',
                values='profit_millions'
            )
            pivot_profit.plot(ax=ax2, marker='o')
            ax2.set_title(f'Profit by Service Type in {region.title()} - {segment.title()}')
            ax2.set_ylabel('Profit (Millions USD)')
            ax2.set_xlabel('Year')
            
            plt.tight_layout()
            
            # Save the figure
            output_path = output_dir / f'economics_{region.lower()}_{segment.lower()}.png'
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Saved economics plot to: {output_path}")

def main():
    # Set up paths
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'src' / 'data' / 'processed_data' / 'new_mobility'
    output_dir = project_root / 'reports' / 'figures' / 'new_mobility'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load the data
    print("Loading data...")
    data = load_data(data_dir)
    
    # Generate plots
    print("\nGenerating service adoption plots...")
    plot_service_adoption(data['service_adoption'], output_dir)
    
    print("\nGenerating ownership model plots...")
    plot_ownership_evolution(data['ownership'], output_dir)
    
    print("\nGenerating economic metrics plots...")
    plot_economic_metrics(data['economics'], output_dir)
    
    print("\nAll visualizations have been generated!")

if __name__ == "__main__":
    main()
