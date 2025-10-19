"""
Setup configuration for the decision-making tool.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="decision-making",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python tool for decision making using Monte Carlo simulations and matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/decision-making",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (currently none - using built-in sqlite3)
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
        "simulation": [
            # Future dependencies for Monte Carlo simulations
            # "numpy>=1.24.0",
            # "scipy>=1.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "decision-making=decision_making.main:example_usage",
        ],
    },
)

