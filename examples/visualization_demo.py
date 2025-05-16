"""
Visualization Demo

This script demonstrates how to use the visualization modules to create
various plots and dashboards for automotive consulting analysis.
"""
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import visualization modules
from src.visualization import plot_utils
from src.visualization.dashboard import ConsultingDashboard, create_scenario_comparison

def generate_sample_data():
    """Generate sample data for demonstration purposes."""
    # Sample market data
    years = list(range(2023, 2031))
    service_types = ["Strategy", "Digital", "Operations", "Technology", "Analytics"]
    
    market_data = []
    for year in years:
        for service in service_types:
            base_size = 10 * (1.1 ** (year - 2023)) * (service_types.index(service) + 1)
            market_data.append({
                'year': year,
                'service_type': service,
                'market_size': base_size * (0.9 + 0.2 * np.random.random()),
                'growth_rate': 0.05 + 0.1 * np.random.random()
            })
    
    market_df = pd.DataFrame(market_data)
    
    # Sample strategy data
    strategy_data = pd.DataFrame({
        'initiative': [f"Initiative {i+1}" for i in range(5)],
        'progress': np.random.uniform(0.3, 0.9, 5),
        'budget_utilization': np.random.uniform(0.4, 1.1, 5),
        'impact': np.random.uniform(3, 10, 5)
    })
    
    # Sample capability data
    capabilities = [
        'Digital Transformation', 'Data Analytics', 'Change Management',
        'Technology Integration', 'Strategy Development'
    ]
    
    capability_data = pd.DataFrame({
        'capability': capabilities,
        'current': np.random.uniform(1, 4, len(capabilities)),
        'target': np.random.uniform(3, 5, len(capabilities))
    })
    
    return {
        'market_data': market_df,
        'strategy_data': strategy_data,
        'capability_data': capability_data
    }

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent

def demo_plot_utils():
    """Demonstrate the plot_utils module."""
    print("Generating sample plots using plot_utils...")
    
    # Set up project-relative paths
    project_root = get_project_root()
    output_dir = project_root / "reports" / "figures" / "demo_plots"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sample data
    data = generate_sample_data()
    market_df = data['market_data']
    
    # 1. Time series plot
    print("Creating time series plot...")
    fig_ts = plot_utils.plot_time_series(
        data=market_df[market_df['service_type'] == 'Strategy'],
        x='year',
        y='market_size',
        title='Strategy Consulting Market Size Over Time',
        xlabel='Year',
        ylabel='Market Size ($B)',
        output_file=output_dir / 'time_series_plot',
        output_dir=output_dir
    )
    
    # 2. Heatmap
    print("Creating heatmap...")
    fig_hm = plot_utils.plot_heatmap(
        data=market_df,
        x='year',
        y='service_type',
        values='market_size',
        title='Market Size by Service Type and Year',
        xlabel='Year',
        ylabel='Service Type',
        output_file=output_dir / 'heatmap_plot',
        output_dir=output_dir
    )
    
    # 3. Radar chart
    print("Creating radar chart...")
    categories = ['Strategy', 'Digital', 'Operations', 'Technology', 'Analytics']
    values = [0.8, 0.6, 0.7, 0.5, 0.9]  # Sample values between 0 and 1
    
    fig_radar = plot_utils.plot_radar_chart(
        categories=categories,
        values=values,
        title='Service Capability Assessment',
        output_file=output_dir / 'radar_chart',
        output_dir=output_dir
    )
    
    # 4. Waterfall chart
    print("Creating waterfall chart...")
    waterfall_data = {
        'Start': 100,
        'New Clients': 30,
        'Upsell': 20,
        'Churn': -15,
        'Price Changes': 5,
        'End': 140
    }
    
    fig_waterfall = plot_utils.plot_waterfall(
        data=waterfall_data,
        title='Revenue Bridge Analysis',
        ylabel='Revenue ($M)',
        output_file=output_dir / 'waterfall_chart',
        output_dir=output_dir
    )
    
    print(f"Plots saved to: {output_dir.relative_to(project_root)}")

def demo_dashboard():
    """Demonstrate the dashboard module."""
    print("Generating interactive dashboards...")
    
    # Set up project-relative paths
    project_root = get_project_root()
    output_dir = project_root / "reports" / "dashboards"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sample data
    data = generate_sample_data()
    
    # Initialize dashboard
    dashboard = ConsultingDashboard(output_dir=output_dir)
    
    # 1. Market overview dashboard
    print("Creating market overview dashboard...")
    fig_market = dashboard.create_market_overview(
        market_data=data['market_data'],
        title="Automotive Consulting Market Overview (2023-2030)"
    )
    dashboard.save_dashboard(fig_market, "market_overview.html")
    
    # 2. Strategy dashboard
    print("Creating strategy dashboard...")
    fig_strategy = dashboard.create_strategy_dashboard(
        strategy_data=data['strategy_data'],
        capability_data=data['capability_data'],
        title="Strategic Initiative Dashboard"
    )
    dashboard.save_dashboard(fig_strategy, "strategy_dashboard.html")
    
    # 3. Scenario comparison
    print("Creating scenario comparison...")
    scenarios = {
        'Base Case': data['market_data'].copy(),
        'Growth': data['market_data'].copy(),
        'Decline': data['market_data'].copy()
    }
    
    # Modify scenarios
    scenarios['Growth']['market_size'] = scenarios['Growth']['market_size'] * 1.5
    scenarios['Decline']['market_size'] = scenarios['Decline']['market_size'] * 0.7
    
    fig_scenario = create_scenario_comparison(
        scenarios=scenarios,
        metric='market_size',
        title='Market Size Scenarios (2023-2030)'
    )
    
    # Save the scenario comparison
    scenario_path = output_dir / 'scenario_comparison.html'
    fig_scenario.write_html(
        str(scenario_path),
        full_html=True,
        include_plotlyjs='cdn',
        config={'displayModeBar': True}
    )
    
    print(f"Dashboards saved to: {output_dir.relative_to(project_root)}")

if __name__ == "__main__":
    # Set up project directory structure
    project_root = get_project_root()
    (project_root / "reports" / "figures").mkdir(parents=True, exist_ok=True)
    (project_root / "reports" / "dashboards").mkdir(parents=True, exist_ok=True)
    
    try:
        # Run demos
        demo_plot_utils()
        demo_dashboard()
        
        print("\nVisualization demo completed successfully!")
        print(f"Outputs saved to: {project_root / 'reports'}")
    except Exception as e:
        print(f"\nError during visualization demo: {str(e)}")
        raise
