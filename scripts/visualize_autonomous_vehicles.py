"""
Autonomous Vehicle Adoption Visualization

This script creates visualizations for the autonomous vehicle adoption simulation results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
import numpy as np
from typing import Dict, List, Optional

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed_data" / "autonomous_vehicles"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures" / "autonomous_vehicles"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data() -> Dict[str, pd.DataFrame]:
    """Load all autonomous vehicle adoption data."""
    data = {}
    
    # Load all CSV files in the directory
    for file in DATA_DIR.glob("*.csv"):
        if file.name == "av_adoption_summary.csv":
            continue  # Skip the summary file
            
        segment = file.stem.replace("av_adoption_", "").replace("_", " ").title()
        try:
            df = pd.read_csv(file)
            data[segment] = df
            print(f"Loaded {segment} data with {len(df)} rows")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    if not data:
        print("No data files found. Please run the simulation first.")
    
    return data

def plot_adoption_curves(data: Dict[str, pd.DataFrame]) -> None:
    """Plot adoption curves for each SAE level by segment."""
    # Combine all segments into one DataFrame for easier plotting
    all_data = []
    for segment, df in data.items():
        df_segment = df.copy()
        df_segment['Segment'] = segment
        all_data.append(df_segment)
    
    df_combined = pd.concat(all_data, ignore_index=True)
    
    # Melt the DataFrame for easier plotting
    id_vars = ['Year', 'Segment']
    value_vars = [col for col in df_combined.columns if col.startswith('SAE ')]
    df_melted = pd.melt(
        df_combined, 
        id_vars=id_vars, 
        value_vars=value_vars,
        var_name='SAE Level',
        value_name='Adoption Rate'
    )
    
    # Create the plot
    plt.figure(figsize=(16, 10))
    
    # Use a color palette that's colorblind-friendly
    palette = sns.color_palette("husl", len(value_vars))
    
    # Create a grid of subplots, one for each segment
    segments = df_melted['Segment'].unique()
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    axes = axes.flatten()
    
    for i, segment in enumerate(segments):
        if i >= len(axes):
            break
            
        ax = axes[i]
        segment_data = df_melted[df_melted['Segment'] == segment]
        
        sns.lineplot(
            data=segment_data,
            x='Year',
            y='Adoption Rate',
            hue='SAE Level',
            style='SAE Level',
            markers=True,
            dashes=False,
            palette=palette,
            ax=ax
        )
        
        ax.set_title(f'Autonomous Vehicle Adoption - {segment}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Adoption Rate')
        ax.set_ylim(0, 1.05)
        ax.legend(title='SAE Level', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'av_adoption_by_segment.png'
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"\nSaved adoption curves by segment to: {output_path}")

def plot_sae_level_heatmap(data: Dict[str, pd.DataFrame]) -> None:
    """Create a heatmap of SAE level adoption by year and segment."""
    # Load the summary data
    summary_file = DATA_DIR / "av_adoption_summary.csv"
    if not summary_file.exists() or os.path.getsize(summary_file) == 0:
        print("Summary file not found or is empty. Please run the simulation first.")
        return
    
    try:
        df_summary = pd.read_csv(summary_file)
        if df_summary.empty:
            print("Summary data is empty. Please run the simulation first.")
            return
    except Exception as e:
        print(f"Error reading summary file: {e}")
        return
    
    # Pivot the data for heatmap
    pivot_2030 = df_summary.pivot(index='Segment', columns='SAE Level', values='Adoption 2030')
    pivot_2040 = df_summary.pivot(index='Segment', columns='SAE Level', values='Adoption 2040')
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Plot heatmaps
    sns.heatmap(pivot_2030, annot=True, cmap='YlOrRd', fmt='.2f', ax=ax1, cbar=False)
    ax1.set_title('SAE Level Adoption in 2030')
    
    sns.heatmap(pivot_2040, annot=True, cmap='YlOrRd', fmt='.2f', ax=ax2, cbar=False)
    ax2.set_title('SAE Level Adoption in 2040')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = OUTPUT_DIR / 'sae_level_heatmap.png'
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"\nSaved SAE level heatmap to: {output_path}")

def plot_autonomy_transition(data: Dict[str, pd.DataFrame]) -> None:
    """Plot the transition between different autonomy levels over time."""
    # Combine all segments into one DataFrame for easier plotting
    all_data = []
    for segment, df in data.items():
        df_segment = df.copy()
        df_segment['Segment'] = segment
        all_data.append(df_segment)
    
    df_combined = pd.concat(all_data, ignore_index=True)
    
    # Calculate the weighted average autonomy level
    sae_columns = [col for col in df_combined.columns if col.startswith('SAE ')]
    for i, col in enumerate(sae_columns):
        df_combined[col] = df_combined[col] * i  # Weight by SAE level
    
    df_combined['Avg_Autonomy'] = df_combined[sae_columns].sum(axis=1)
    
    # Plot the transition
    plt.figure(figsize=(14, 8))
    
    sns.lineplot(
        data=df_combined,
        x='Year',
        y='Avg_Autonomy',
        hue='Segment',
        style='Segment',
        markers=True,
        dashes=False,
        linewidth=2.5
    )
    
    # Add SAE level annotations
    sae_levels = {
        0: 'No Automation',
        1: 'Driver Assistance',
        2: 'Partial Automation',
        3: 'Conditional Automation',
        4: 'High Automation',
        5: 'Full Automation'
    }
    
    for level, label in sae_levels.items():
        plt.axhline(y=level, color='gray', linestyle='--', alpha=0.3)
        plt.text(2040.5, level, f"{label} (SAE {level})", va='center', ha='left', color='gray')
    
    plt.title('Average Autonomous Vehicle Capability by Segment (2025-2040)')
    plt.xlabel('Year')
    plt.ylabel('Average SAE Autonomy Level')
    plt.ylim(-0.2, 5.2)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Save the figure
    output_path = OUTPUT_DIR / 'autonomy_transition.png'
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"\nSaved autonomy transition plot to: {output_path}")

def main():
    print("Loading autonomous vehicle data...")
    data = load_data()
    
    if not data:
        return
    
    print("\nGenerating visualizations...")
    plot_adoption_curves(data)
    plot_sae_level_heatmap(data)
    plot_autonomy_transition(data)
    
    print("\nAll visualizations have been generated!")

if __name__ == "__main__":
    main()
