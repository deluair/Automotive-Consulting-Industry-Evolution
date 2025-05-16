"""
Dashboard Module for Automotive Consulting Analysis

This module provides functions to create interactive dashboards for visualizing
simulation results and strategic analyses.
"""
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Import local modules
from . import plot_utils

class ConsultingDashboard:
    """A class to create interactive dashboards for consulting analysis."""
    
    def __init__(self, output_dir: Union[str, Path] = "output"):
        """Initialize the dashboard with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_market_overview(
        self,
        market_data: pd.DataFrame,
        title: str = "Automotive Consulting Market Overview"
    ) -> go.Figure:
        """Create an overview dashboard of the consulting market.
        
        Args:
            market_data: DataFrame containing market data with columns:
                        ['year', 'service_type', 'market_size', 'growth_rate']
            title: Dashboard title
            
        Returns:
            Plotly Figure object
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "pie"}, {"type": "bar"}],
                  [{"colspan": 2}, None]],
            subplot_titles=(
                "Market Share by Service Type",
                "Growth Rate by Service Type",
                "Market Size Over Time"
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Get the latest year's data
        latest_year = market_data['year'].max()
        latest_data = market_data[market_data['year'] == latest_year]
        
        # 1. Pie chart - Market share
        fig.add_trace(
            go.Pie(
                labels=latest_data['service_type'],
                values=latest_data['market_size'],
                name="Market Share",
                hole=0.4,
                showlegend=False
            ),
            row=1, col=1
        )
        
        # 2. Bar chart - Growth rate
        fig.add_trace(
            go.Bar(
                x=latest_data['service_type'],
                y=latest_data['growth_rate'],
                name="Growth Rate",
                text=latest_data['growth_rate'].apply(lambda x: f"{x:.1%}"),
                textposition='auto',
                marker_color=px.colors.qualitative.Plotly[1:]
            ),
            row=1, col=2
        )
        
        # 3. Line chart - Market size over time
        for service in market_data['service_type'].unique():
            service_data = market_data[market_data['service_type'] == service]
            fig.add_trace(
                go.Scatter(
                    x=service_data['year'],
                    y=service_data['market_size'],
                    mode='lines+markers',
                    name=service,
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                y=0.95,
                font=dict(size=20)
            ),
            height=800,
            width=1000,
            margin=dict(t=100, b=50, l=50, r=50),
            plot_bgcolor='white'
        )
        
        # Update y-axes
        fig.update_yaxes(title_text="Market Size ($B)", row=2, col=1)
        fig.update_yaxes(title_text="Growth Rate", row=1, col=2, tickformat=".0%")
        
        # Update x-axes
        fig.update_xaxes(title_text="Service Type", row=1, col=2)
        fig.update_xaxes(title_text="Year", row=2, col=1)
        
        # Rotate x-axis labels
        fig.update_xaxes(tickangle=45, row=1, col=2)
        
        return fig
    
    def create_strategy_dashboard(
        self,
        strategy_data: pd.DataFrame,
        capability_data: pd.DataFrame,
        title: str = "Strategic Initiative Dashboard"
    ) -> go.Figure:
        """Create a dashboard for strategic initiatives and capabilities.
        
        Args:
            strategy_data: DataFrame with strategy metrics
            capability_data: DataFrame with capability assessment
            title: Dashboard title
            
        Returns:
            Plotly Figure object
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                  [{"type": "bar"}, {"type": "scatterpolar"}]],
            subplot_titles=(
                "Overall Progress",
                "Budget Utilization",
                "Capability Maturity",
                "Strategic Balance"
            ),
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # 1. Overall progress indicator
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=strategy_data['progress'].mean() * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Progress"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "gray"},
                        {'range': [75, 100], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=1, col=1
        )
        
        # 2. Budget utilization indicator
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=strategy_data['budget_utilization'].mean() * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Budget Utilization"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgreen"},
                        {'range': [60, 90], 'color': "green"},
                        {'range': [90, 100], 'color': "darkgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 85
                    }
                }
            ),
            row=1, col=2
        )
        
        # 3. Capability maturity bar chart
        fig.add_trace(
            go.Bar(
                x=capability_data['capability'],
                y=capability_data['current'],
                name="Current",
                marker_color='lightblue',
                text=capability_data['current'],
                textposition='auto'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=capability_data['capability'],
                y=capability_data['target'] - capability_data['current'],
                name="Gap",
                marker_color='lightcoral',
                text=capability_data['target'],
                textposition='auto'
            ),
            row=2, col=1
        )
        
        # 4. Strategic balance radar chart
        categories = capability_data['capability'].tolist()
        
        fig.add_trace(
            go.Scatterpolar(
                r=capability_data['current'].tolist(),
                theta=categories,
                fill='toself',
                name='Current',
                line=dict(color='blue')
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatterpolar(
                r=capability_data['target'].tolist(),
                theta=categories,
                fill='toself',
                name='Target',
                line=dict(color='red', dash='dash')
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                y=0.95,
                font=dict(size=20)
            ),
            height=800,
            width=1200,
            margin=dict(t=100, b=50, l=50, r=50),
            plot_bgcolor='white',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Update subplot titles
        fig.update_annotations(font_size=12)
        
        # Update y-axes
        fig.update_yaxes(title_text="Maturity Level (1-5)", row=2, col=1, range=[0, 5])
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray', row=2, col=2)
        
        # Update x-axes
        fig.update_xaxes(tickangle=45, row=2, col=1)
        
        return fig
    
    def save_dashboard(self, fig: go.Figure, filename: str) -> Path:
        """Save the dashboard to an HTML file.
        
        Args:
            fig: Plotly Figure object
            filename: Output filename (without extension)
            
        Returns:
            Path to the saved file
        """
        if not filename.endswith('.html'):
            filename += '.html'
            
        filepath = self.output_dir / filename
        fig.write_html(
            filepath,
            full_html=True,
            include_plotlyjs='cdn',
            config={'displayModeBar': True}
        )
        return filepath


def create_scenario_comparison(
    scenarios: Dict[str, pd.DataFrame],
    metric: str = "market_size",
    title: str = "Scenario Comparison"
) -> go.Figure:
    """Create a comparison chart of different scenarios.
    
    Args:
        scenarios: Dictionary of scenario names to DataFrames
        metric: The metric to compare
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    for scenario_name, df in scenarios.items():
        fig.add_trace(
            go.Scatter(
                x=df['year'],
                y=df[metric],
                mode='lines+markers',
                name=scenario_name,
                hovertemplate='%{x}<br>' + f'{metric}: %{{y:,.0f}}<extra></extra>'
            )
        )
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            y=0.95,
            font=dict(size=20)
        ),
        xaxis_title="Year",
        yaxis_title=metric.replace('_', ' ').title(),
        legend_title="Scenario",
        hovermode="x unified",
        template="plotly_white",
        height=600,
        width=1000
    )
    
    return fig
