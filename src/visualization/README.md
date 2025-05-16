# Visualization Module

This module provides tools for creating visualizations and dashboards for the Automotive Consulting Simulation project.

## Features

- **plot_utils.py**: A collection of utility functions for creating static visualizations using Matplotlib and Seaborn.
- **dashboard.py**: A class-based API for creating interactive dashboards using Plotly.
- Example scripts demonstrating usage of the visualization tools.

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements-visualization.txt
```

## Usage

### Basic Plotting with plot_utils

```python
from src.visualization import plot_utils
import pandas as pd

# Sample data
data = pd.DataFrame({
    'year': [2023, 2024, 2025, 2026, 2027],
    'value': [100, 150, 200, 180, 250]
})

# Create a time series plot
fig = plot_utils.plot_time_series(
    data=data,
    x='year',
    y='value',
    title='Sample Time Series',
    xlabel='Year',
    ylabel='Value ($M)'
)
```

### Creating Dashboards

```python
from src.visualization.dashboard import ConsultingDashboard
import pandas as pd

# Sample data
market_data = pd.DataFrame({
    'year': [2023, 2023, 2024, 2024],
    'service_type': ['Strategy', 'Digital', 'Strategy', 'Digital'],
    'market_size': [100, 150, 110, 160],
    'growth_rate': [0.05, 0.07, 0.06, 0.08]
})

# Create and save a dashboard
dashboard = ConsultingDashboard(output_dir='output')
fig = dashboard.create_market_overview(market_data, title='Market Overview')
dashboard.save_dashboard(fig, 'market_overview.html')
```

## Running the Demo

A demo script is available in the `examples` directory that demonstrates the capabilities of the visualization module:

```bash
python examples/visualization_demo.py
```

This will generate sample visualizations and save them to the `output` directory.

## Plot Types

The module supports various plot types including:

- Time series plots
- Bar charts
- Heatmaps
- Radar charts
- Waterfall charts
- Interactive dashboards with multiple visualizations

## Dependencies

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- plotly

## License

This project is licensed under the MIT License - see the LICENSE file for details.
