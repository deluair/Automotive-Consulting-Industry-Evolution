"""
Simple Report Generator Module

This module provides functionality to generate comprehensive HTML reports with interactive visualizations,
tables, and text content. It uses Plotly for visualizations and a simplified template approach.
"""
import os
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

import plotly.graph_objects as go


class SimpleReportGenerator:
    """
    A simple class to generate comprehensive HTML reports with visualizations and analysis.
    """

    def __init__(self, title: str = "Automotive Industry Report"):
        """
        Initialize the SimpleReportGenerator with a title.

        Args:
            title (str): The title of the report
        """
        self.title = title
        self.sections = []
        self.figures = []
        self.tables = []
        self.now = datetime.now()

    def add_section(self, title: str, content: str = "", level: int = 1) -> None:
        """
        Add a section to the report.

        Args:
            title (str): Section title
            content (str): HTML content of the section
            level (int): Heading level (1 for h1, 2 for h2, etc.)
        """
        self.sections.append({
            "title": title,
            "content": content,
            "level": level,
        })

    def add_figure(self, fig: go.Figure, title: str, caption: str = "") -> str:
        """
        Add a Plotly figure to the report.

        Args:
            fig (go.Figure): Plotly figure object
            title (str): Figure title
            caption (str, optional): Figure caption/description

        Returns:
            str: The ID of the added figure
        """
        figure_id = f"figure-{len(self.figures) + 1}"
        self.figures.append({
            "id": figure_id,
            "figure": fig,
            "title": title,
            "caption": caption,
        })
        return figure_id

    def _get_html_template(self) -> str:
        """Get the HTML template for the report."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            padding: 20px;
        }
        .report-header {
            background-color: #f8f9fa;
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid #dee2e6;
        }
        .section {
            margin-bottom: 3rem;
        }
        .figure-container {
            margin: 2rem 0;
            padding: 1.5rem;
            background-color: #fff;
            border-radius: 0.5rem;
            box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        }
        .figure-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2c3e50;
        }
        .figure-caption {
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #6c757d;
        }
        .table-container {
            margin: 2rem 0;
            overflow-x: auto;
        }
        .table {
            font-size: 0.9rem;
        }
        .table th {
            background-color: #f8f9fa;
            font-weight: 600;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        h1 { font-size: 2.2rem; }
        h2 { font-size: 1.8rem; }
        h3 { font-size: 1.5rem; }
        h4 { font-size: 1.3rem; }
        h5 { font-size: 1.1rem; }
        .toc {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        .toc-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2c3e50;
        }
        .toc-list {
            list-style-type: none;
            padding-left: 0;
        }
        .toc-list li {
            margin-bottom: 0.5rem;
        }
        .toc-list a {
            color: #3498db;
            text-decoration: none;
        }
        .toc-list a:hover {
            text-decoration: underline;
        }
        footer {
            margin-top: 4rem;
            padding: 2rem 0;
            background-color: #f8f9fa;
            text-align: center;
            color: #6c757d;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <!-- Header -->
    <div class="report-header">
        <div class="container">
            <h1 class="display-4">{{title}}</h1>
            <p class="lead text-muted">Generated on {{now}}</p>
        </div>
    </div>

    <div class="container">
        <!-- Table of Contents -->
        <div class="toc">
            <div class="toc-title">Table of Contents</div>
            <ul class="toc-list">
                {% for section in sections %}
                <li style="margin-left: {{ (section.level - 1) * 1.5 }}rem;">
                    <a href="#section-{{ loop.index }}">{{ section.title }}</a>
                </li>
                {% endfor %}
                {% if figures %}
                <li style="margin-left: 1.5rem;">
                    <a href="#visualizations">Visualizations</a>
                </li>
                {% endif %}
                {% if tables %}
                <li style="margin-left: 1.5rem;">
                    <a href="#tables">Data Tables</a>
                </li>
                {% endif %}
            </ul>
        </div>

        <!-- Report Content -->
        <div class="report-content">
            {% for section in sections %}
            <div id="section-{{ loop.index }}" class="section">
                <h{{ section.level }}>{{ section.title }}</h{{ section.level }}>
                {{ section.content | safe }}
            </div>
            {% endfor %}

            <!-- Figures -->
            {% if figures %}
            <div id="visualizations" class="section">
                <h2>Visualizations</h2>
                {% for fig in figures %}
                <div class="figure-container">
                    <div class="figure-title">{{ fig.title }}</div>
                    <div id="{{ fig.id }}"></div>
                    {% if fig.caption %}
                    <div class="figure-caption">{{ fig.caption }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <!-- Tables -->
            {% if tables %}
            <div id="tables" class="section">
                <h2>Data Tables</h2>
                {% for table in tables %}
                <div class="table-container">
                    <div class="figure-title">{{ table.title }}</div>
                    <div class="table-responsive">
                        {{ table.data | safe }}
                    </div>
                    {% if table.caption %}
                    <div class="figure-caption">{{ table.caption }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </div>

    <footer>
        <div class="container">
            <p>Report generated on {{now}}</p>
            <p>© 2025 Automotive Consulting Industry Evolution Analysis</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Initialize all Plotly figures
        document.addEventListener('DOMContentLoaded', function() {
            {% for fig in figures %}
                var figure = {{ fig.figure.to_json() | safe }};
                Plotly.newPlot('{{ fig.id }}', figure.data, figure.layout);
            {% endfor %}
        });
    </script>
</body>
</html>"""

    def generate_report(self, output_file: Union[str, Path]) -> None:
        """
        Generate the HTML report.

        Args:
            output_file: Path where the HTML report will be saved
        """
        from jinja2 import Template
        
        # Convert output_file to Path object if it's a string
        output_file = Path(output_file) if isinstance(output_file, str) else output_file
        
        # Ensure the output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Get the template
        template = Template(self._get_html_template())
        
        # Prepare the context
        context = {
            'title': self.title,
            'sections': self.sections,
            'figures': self.figures,
            'tables': self.tables,
            'now': self.now.strftime('%B %d, %Y %H:%M:%S'),
        }
        
        # Render the template
        html_content = template.render(**context)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report generated successfully: {output_file.absolute()}")

    def open_in_browser(self, output_file: Union[str, Path]) -> None:
        """
        Open the generated report in the default web browser.

        Args:
            output_file: Path to the generated HTML report
        """
        output_file = str(Path(output_file).absolute())
        webbrowser.open(f"file://{output_file}")

    def generate_and_open(self, output_file: Union[str, Path]) -> None:
        """
        Generate the report and open it in the default web browser.

        Args:
            output_file: Path where the HTML report will be saved
        """
        self.generate_report(output_file)
        self.open_in_browser(output_file)
