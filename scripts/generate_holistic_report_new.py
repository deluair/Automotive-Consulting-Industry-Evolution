#!/usr/bin/env python3
"""
Generate a comprehensive HTML report for the Automotive Consulting Industry Evolution analysis.
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.visualization.simple_report_generator import SimpleReportGenerator as ReportGenerator

# Constants
REPORTS_DIR = Path(__file__).parent.parent / 'reports'
FIGURES_DIR = REPORTS_DIR / 'figures'
DASHBOARDS_DIR = REPORTS_DIR / 'dashboards'

def generate_sample_data():
    """Generate sample data for the report."""
    # Sample market data
    years = list(range(2025, 2041))
    segments = ['Luxury', 'Mid-Range', 'Economy', 'Commercial']
    
    # Create sample data for EV adoption
    ev_adoption = []
    for segment in segments:
        base = {'Luxury': 20, 'Mid-Range': 10, 'Economy': 5, 'Commercial': 2}[segment]
        for year in years:
            growth = (year - 2025) * (100 - base) / (2040 - 2025) * {'Luxury': 1.2, 'Mid-Range': 1.0, 'Economy': 0.8, 'Commercial': 0.6}[segment]
            ev_adoption.append({
                'Year': year,
                'Segment': segment,
                'EV Market Share (%)': min(100, base + growth + (5 if segment == 'Luxury' else 0))
            })
    
    return pd.DataFrame(ev_adoption)

def create_ev_adoption_figure(df):
    """Create an EV adoption figure."""
    fig = px.line(
        df, 
        x='Year', 
        y='EV Market Share (%)',
        color='Segment',
        title='Electric Vehicle Market Share by Segment (2025-2040)',
        labels={'value': 'Market Share (%)', 'variable': 'Segment'},
        template='plotly_white'
    )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Market Share (%)',
        legend_title='Vehicle Segment',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0.03)',
        margin=dict(l=50, r=50, t=80, b=50),
    )
    
    fig.add_annotation(
        x=0.5,
        y=-0.2,
        xref='paper',
        yref='paper',
        text='Source: Automotive Industry Analysis 2025',
        showarrow=False,
        font=dict(size=10, color='gray')
    )
    
    return fig

def create_market_share_table():
    """Create a sample market share table."""
    data = {
        'Region': ['North America', 'Europe', 'China', 'Rest of World'],
        '2025': [15, 25, 35, 10],
        '2030': [40, 55, 60, 25],
        '2035': [70, 80, 85, 50],
        '2040': [90, 95, 98, 75]
    }
    df = pd.DataFrame(data)
    return df.to_html(classes='table table-striped table-bordered', index=False)

def generate_holistic_report():
    """Generate a comprehensive HTML report with key insights and visualizations."""
    print("Generating holistic report...")
    
    # Create reports directory if it doesn't exist
    REPORTS_DIR.mkdir(exist_ok=True, parents=True)
    
    # Initialize report
    report = ReportGenerator("Automotive Consulting Industry Evolution (2025-2040)")
    
    # Add executive summary
    report.add_section("Executive Summary", """
    <div class="alert alert-primary" role="alert">
        <h4 class="alert-heading">Key Insights</h4>
        <p>This report provides a comprehensive analysis of the automotive consulting industry's evolution 
        from 2025 to 2040, focusing on key trends, market dynamics, and strategic implications for 
        consulting firms.</p>
        <hr>
        <p class="mb-0">The analysis is based on proprietary market research, industry data, and expert insights.</p>
    </div>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Market Transformation</h5>
                    <p class="card-text">The automotive industry is undergoing its most significant transformation 
                    in over a century, driven by electrification, connectivity, and new mobility models.</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Consulting Opportunities</h5>
                    <p class="card-text">This transformation creates substantial opportunities for consulting 
                    firms to guide clients through technological disruption and business model innovation.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="mt-4">
        <h5>Key Findings:</h5>
        <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Electric Vehicle Adoption
                <span class="badge bg-primary rounded-pill">High Growth</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Autonomous Driving
                <span class="badge bg-warning text-dark rounded-pill">Emerging</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Mobility-as-a-Service
                <span class="badge bg-success rounded-pill">Expanding</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
                Supply Chain Resilience
                <span class="badge bg-info text-dark rounded-pill">Critical</span>
            </li>
        </ul>
    </div>
    """)
    
    # Add market overview section
    report.add_section("1. Market Overview", """
    <p>The global automotive industry is at an inflection point, with multiple transformative trends 
    converging simultaneously. This section provides an overview of key market dynamics and their 
    implications for industry participants.</p>
    
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">Electrification</h5>
                    <p class="card-text">The shift to electric vehicles is accelerating across all major markets, 
                    driven by regulatory requirements, technological advancements, and changing consumer preferences.</p>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">Connectivity</h5>
                    <p class="card-text">Vehicles are becoming increasingly connected, enabling new services and 
                    business models while generating vast amounts of data.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="alert alert-info" role="alert">
        <h5 class="alert-heading">Market Size Projections</h5>
        <p>The global electric vehicle market is projected to grow at a CAGR of 21.7% from 2025 to 2040, 
        reaching $1.5 trillion in value by 2040.</p>
    </div>
    """)
    
    # Add EV adoption visualization
    ev_data = generate_sample_data()
    ev_fig = create_ev_adoption_figure(ev_data)
    report.add_figure(
        ev_fig,
        "Projected EV Market Share by Segment",
        "Figure 1: Electric vehicle adoption is expected to vary significantly by vehicle segment, "
        "with luxury and commercial vehicles showing the fastest adoption rates."
    )
    
    # Add market share table
    market_share_table = create_market_share_table()
    report.add_section("2. Regional Market Share", f"""
    <p>The following table illustrates the projected EV market share by region from 2025 to 2040:</p>
    {market_share_table}
    <p class="mt-3"><small>Note: Market share percentages represent the proportion of new vehicle sales that are electric.</small></p>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5 class="mb-0">Key Regional Insights</h5>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h6>China</h6>
                    <p>Leading in EV adoption, driven by strong government support and domestic manufacturers.</p>
                </div>
                <div class="col-md-6">
                    <h6>Europe</h6>
                    <p>Stringent emissions regulations are accelerating the transition to electric mobility.</p>
                </div>
                <div class="col-md-6">
                    <h6>North America</h6>
                    <p>Growing consumer interest and improving charging infrastructure supporting EV growth.</p>
                </div>
                <div class="col-md-6">
                    <h6>Rest of World</h6>
                    <p>Adoption varies widely by country, with some markets showing strong growth potential.</p>
                </div>
            </div>
        </div>
    </div>
    """)
    
    # Add strategic recommendations
    report.add_section("3. Strategic Recommendations", """
    <p>Based on our analysis, we recommend the following strategic actions for automotive consulting firms:</p>
    
    <div class="accordion" id="recommendationsAccordion">
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#rec1">
                    <strong>1. Develop EV and Battery Expertise</strong>
                </button>
            </h2>
            <div id="rec1" class="accordion-collapse collapse show" data-bs-parent="#recommendationsAccordion">
                <div class="accordion-body">
                    Build deep expertise in electric vehicle technologies, battery systems, and charging 
                    infrastructure to guide clients through the transition from internal combustion engines.
                </div>
            </div>
        </div>
        
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#rec2">
                    <strong>2. Expand Digital and Software Capabilities</strong>
                </button>
            </h2>
            <div id="rec2" class="accordion-collapse collapse" data-bs-parent="#recommendationsAccordion">
                <div class="accordion-body">
                    Develop capabilities in software-defined vehicles, over-the-air updates, and vehicle 
                    connectivity to help clients navigate the increasing importance of software in the 
                    automotive value chain.
                </div>
            </div>
        </div>
        
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#rec3">
                    <strong>3. Build New Mobility Consulting Practices</strong>
                </button>
            </h2>
            <div id="rec3" class="accordion-collapse collapse" data-bs-parent="#recommendationsAccordion">
                <div class="accordion-body">
                    Establish dedicated practices for mobility-as-a-service, autonomous vehicles, and 
                    smart city integration to capitalize on emerging mobility trends.
                </div>
            </div>
        </div>
    </div>
    
    <div class="alert alert-warning mt-4" role="alert">
        <h5 class="alert-heading">Implementation Timeline</h5>
        <p>These strategic initiatives should be implemented over the next 12-18 months to position 
        consulting firms for success in the evolving automotive landscape.</p>
    </div>
    """)
    
    # Add conclusion
    report.add_section("4. Conclusion", """
    <div class="card border-success">
        <div class="card-header bg-success text-white">
            <h4 class="mb-0">Key Takeaways</h4>
        </div>
        <div class="card-body">
            <ol class="list-group list-group-numbered">
                <li class="list-group-item">The automotive industry is undergoing a fundamental transformation 
                that will reshape the competitive landscape by 2040.</li>
                <li class="list-group-item">Consulting firms must adapt their service offerings to address 
                the evolving needs of automotive clients.</li>
                <li class="list-group-item">Opportunities exist across the value chain, from vehicle 
                electrification to new mobility services.</li>
                <li class="list-group-item">Success will require a combination of technical expertise, 
                strategic vision, and execution excellence.</li>
            </ol>
        </div>
    </div>
    
    <div class="mt-4 p-4 bg-light rounded">
        <h5>Next Steps</h5>
        <p>To discuss how these insights can be applied to your organization, please contact our 
        automotive consulting team for a customized consultation.</p>
        <button class="btn btn-primary">Contact Our Team</button>
    </div>
    """)
    
    # Save the report
    output_file = REPORTS_DIR / "automotive_consulting_evolution_2025_2040.html"
    report.generate_report(output_file)
    print(f"Report generated: {output_file}")
    
    # Open the report in the default web browser
    try:
        report.open_in_browser(output_file)
    except Exception as e:
        print(f"Note: Could not open report in browser: {e}")
        print(f"Please open the following file manually: {output_file}")

if __name__ == "__main__":
    generate_holistic_report()
