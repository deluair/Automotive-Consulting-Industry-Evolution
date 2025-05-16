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

# ... rest of the code remains the same ...
    
    # Add industry transformation section
    report.add_section("1. Industry Transformation", """
    <p>The automotive industry is undergoing its most significant transformation in over a century, driven by 
    technological disruption, changing consumer preferences, and regulatory pressures. This section examines 
    the key trends reshaping the industry landscape.</p>
    """, level=1)
    
    # Add EV adoption chart
    ev_fig = create_industry_overview()
    report.add_figure(ev_fig, "Electric Vehicle Adoption by Segment (2025-2040)", 
                     "Projected EV adoption rates across different vehicle segments, showing the rapid transition "
                     "from internal combustion engines to electric powertrains.")
    
    # Add AV adoption chart
    av_fig = create_autonomous_adoption_chart()
    report.add_figure(av_fig, "Autonomous Vehicle Technology Adoption", 
                     "Projected adoption rates for different levels of autonomous driving technology, "
                     "highlighting the gradual progression from driver assistance to full autonomy.")
    
    # Add market share section
    report.add_section("2. Market Share Evolution", """
    <p>The competitive landscape is being reshaped by the emergence of new players and the changing 
    fortunes of traditional automakers. This section analyzes market share trends across regions and 
    manufacturer types.</p>
    """, level=1)
    
    # Add market share chart
    ms_fig = create_market_share_chart()
    report.add_figure(ms_fig, "Automotive Market Share by Region (2025-2040)",
                     "Projected market share evolution by region, showing the growing influence of Chinese "
                     "OEMs and new EV entrants at the expense of traditional automakers.")
    
    # Add strategic recommendations
    report.add_section("3. Strategic Roadmap", """
    <p>Success in the evolving automotive landscape requires a clear strategic roadmap that addresses both 
    near-term challenges and long-term opportunities. This section outlines key strategic initiatives for 
    different time horizons.</p>
    """, level=1)
    
    # Add strategy recommendations chart
    strat_fig = create_strategy_recommendations()
    report.add_figure(strat_fig, "Strategic Roadmap for Automotive OEMs (2025-2040)",
                     "A phased approach to navigating industry transformation, highlighting key focus areas "
                     "and strategic actions for different time horizons.")
    
    # Add key takeaways
    report.add_section("4. Key Takeaways", """
    <h4>Critical Success Factors:</h4>
    <ul>
        <li><b>Accelerated Electrification:</b> Rapid scaling of EV production and battery supply chain</li>
        <li><b>Software & Digital Capabilities:</b> Building in-house software expertise and digital platforms</li>
        <li><b>Business Model Innovation:</b> Developing recurring revenue streams from services and data</li>
        <li><b>Strategic Partnerships:</b> Collaborating across the mobility ecosystem</li>
        <li><b>Supply Chain Resilience:</b> Securing critical materials and regionalizing production</li>
    </ul>
    
    <h4>Risks and Mitigation:</h4>
    <ul>
        <li><b>Technology Disruption:</b> Continuous R&D investment and technology scouting</li>
        <li><b>Regulatory Uncertainty:</b> Scenario planning and policy engagement</li>
        <li><b>Consumer Acceptance:</b> Education, incentives, and compelling product offerings</li>
        <li><b>Cybersecurity Threats:</b> Robust security frameworks and protocols</li>
    </ul>
    
    <p>The automotive industry's transformation presents both significant challenges and opportunities. 
    Companies that can navigate this complexity with agility, foresight, and strategic clarity will be 
    best positioned to thrive in the new mobility era.</p>
    """, level=1)
    
    # Add timestamp
    report.add_section("Report Information", f"""
    <p>Report generated on: {datetime.now().strftime('%B %d, %Y')}</p>
    <p>Data sources: Internal analysis, industry reports, and market research</p>
    <p>For more information, please contact: [Your Contact Information]</p>
    """, level=2)
    
    # Generate and save the report
    output_file = REPORTS_DIR / 'holistic_industry_analysis.html'
    report.generate_report(output_file)
    
    print(f"Report generated successfully: {output_file}")
    
    # Open the report in the default web browser
    webbrowser.open(f'file://{output_file.absolute()}')

if __name__ == "__main__":
    generate_holistic_report()
