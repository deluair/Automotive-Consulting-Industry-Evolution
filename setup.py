from setuptools import setup, find_packages

setup(
    name="automotive_consulting_simulation",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "plotly>=5.0.0",
        "jinja2>=3.0.0",
        "scipy>=1.7.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automotive Consulting Industry Evolution Simulation (2025-2040)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/automotive-consulting-simulation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
