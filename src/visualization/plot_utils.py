"""
Plotting Utilities for Automotive Consulting Analysis

This module provides reusable visualization functions for analyzing and presenting
data from the automotive consulting simulation models.
"""
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set the default style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Color palettes
PALETTE = sns.color_palette("husl", 6)
SNS_PALETTE = sns.color_palette("viridis", 6)


def save_figure(fig: plt.Figure, filename: Union[str, Path], output_dir: Union[str, Path] = "output") -> Path:
    """Save a matplotlib figure to the specified directory.
    
    Args:
        fig: Matplotlib figure to save
        filename: Name of the output file (with or without extension)
        output_dir: Directory to save the figure in
        
    Returns:
        Path to the saved figure
    """
    # Convert to Path objects
    output_path = Path(output_dir)
    filepath = Path(filename)
    
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # If filename is a directory, use default name
    if filepath.is_dir() or str(filepath) == '':
        filepath = output_path / "figure.png"
    # If filename doesn't have an extension, add .png
    elif not filepath.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg', '.pdf']:
        filepath = filepath.with_suffix('.png')
    
    # If filename is not absolute, make it relative to output_dir
    if not filepath.is_absolute():
        filepath = output_path / filepath
    
    # Ensure parent directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the figure
    fig.savefig(str(filepath), bbox_inches='tight', dpi=300, transparent=False)
    plt.close(fig)
    return filepath


def plot_time_series(
    data: pd.DataFrame,
    x: str,
    y: str,
    hue: Optional[str] = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    output_file: Optional[str] = None,
    output_dir: Union[str, Path] = "output",
    **kwargs
) -> plt.Figure:
    """Create a time series plot.
    
    Args:
        data: DataFrame containing the data
        x: Column name for x-axis (typically time)
        y: Column name for y-axis (values to plot)
        hue: Column name to group by (for multiple lines)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        output_file: If provided, save the plot to this file
        output_dir: Directory to save the plot in
        **kwargs: Additional arguments passed to sns.lineplot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=kwargs.pop('figsize', (12, 6)))
    
    # Create the line plot
    sns.lineplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        style=hue if hue else None,
        markers=True,
        dashes=False,
        palette=PALETTE,
        ax=ax,
        **kwargs
    )
    
    # Customize the plot
    ax.set_title(title, pad=20)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels if they're dates
    if pd.api.types.is_datetime64_any_dtype(data[x]):
        plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure if requested
    if output_file:
        save_figure(fig, output_file, output_dir)
    
    return fig


def plot_heatmap(
    data: pd.DataFrame,
    x: str,
    y: str,
    values: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    cmap: str = "YlOrRd",
    fmt: str = ".2f",
    output_file: Optional[str] = None,
    output_dir: Union[str, Path] = "output",
    **kwargs
) -> plt.Figure:
    """Create a heatmap from a DataFrame.
    
    Args:
        data: DataFrame containing the data
        x: Column name for x-axis
        y: Column name for y-axis
        values: Column name for cell values
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        cmap: Color map to use
        fmt: Format string for annotations
        output_file: If provided, save the plot to this file
        output_dir: Directory to save the plot in
        **kwargs: Additional arguments passed to sns.heatmap
        
    Returns:
        Matplotlib figure object
    """
    # Pivot the data for the heatmap
    pivot_data = data.pivot(index=y, columns=x, values=values)
    
    # Create the figure
    fig, ax = plt.subplots(figsize=kwargs.pop('figsize', (10, 8)))
    
    # Create the heatmap
    sns.heatmap(
        pivot_data,
        annot=True,
        cmap=cmap,
        fmt=fmt,
        linewidths=0.5,
        ax=ax,
        **kwargs
    )
    
    # Customize the plot
    ax.set_title(title, pad=20)
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure if requested
    if output_file:
        save_figure(fig, output_file, output_dir)
    
    return fig


def plot_radar_chart(
    categories: List[str],
    values: List[float],
    title: str = "",
    color: str = "blue",
    alpha: float = 0.3,
    output_file: Optional[str] = None,
    output_dir: Union[str, Path] = "output",
) -> plt.Figure:
    """Create a radar (spider) chart.
    
    Args:
        categories: List of category names
        values: List of values for each category (same length as categories)
        title: Plot title
        color: Color of the radar plot
        alpha: Transparency of the filled area
        output_file: If provided, save the plot to this file
        output_dir: Directory to save the plot in
        
    Returns:
        Matplotlib figure object
    """
    N = len(categories)
    
    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the plot
    
    # Initialise the spider plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=7)
    plt.ylim(0, 1)
    
    # Plot data
    values += values[:1]  # Close the plot
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=alpha)
    
    # Add title
    plt.title(title, size=15, color='black', y=1.1)
    
    # Save the figure if requested
    if output_file:
        save_figure(fig, output_file, output_dir)
    
    return fig


def plot_waterfall(
    data: Dict[str, float],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Value",
    output_file: Optional[str] = None,
    output_dir: Union[str, Path] = "output",
) -> plt.Figure:
    """Create a waterfall chart.
    
    Args:
        data: Dictionary with keys as labels and values as the bar heights
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        output_file: If provided, save the plot to this file
        output_dir: Directory to save the plot in
        
    Returns:
        Matplotlib figure object
    """
    # Prepare data
    df = pd.DataFrame({
        'category': list(data.keys()),
        'value': list(data.values())
    })
    
    # Calculate running totals
    df['running_total'] = df['value'].cumsum()
    df['y_start'] = df['running_total'] - df['value']
    
    # Colors
    df['color'] = df['value'].apply(lambda x: 'green' if x > 0 else 'red' if x < 0 else 'gray')
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot bars
    for i, row in df.iterrows():
        ax.bar(
            x=row['category'],
            height=row['value'],
            bottom=row['y_start'],
            color=row['color'],
            alpha=0.6,
            width=0.6
        )
    
    # Add value labels
    for i, row in df.iterrows():
        if row['value'] != 0:  # Skip zero values
            ax.text(
                x=i,
                y=row['running_total'] + (0.02 * df['running_total'].max() * (1 if row['value'] > 0 else -1)),
                s=f"{row['value']:+.2f}",
                ha='center',
                va='bottom' if row['value'] > 0 else 'top'
            )
    
    # Customize the plot
    ax.set_title(title, pad=20)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Add a horizontal line at y=0
    ax.axhline(y=0, color='black', linewidth=0.5)
    
    # Save the figure if requested
    if output_file:
        save_figure(fig, output_file, output_dir)
    
    return fig
