"""
Setup configuration for the strange tool.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="strange",
    version="0.1.0",
    author="João Wiciuk",
    author_email="joaowiciuk@gmail.com",
    description="A probabilistic Multi-Criteria Decision Analysis (MCDA) tool for decision makers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joaowiciuk/strange",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
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
            "strange=strange.main:example_usage",
        ],
    },
)

