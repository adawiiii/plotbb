"""Package configuration for matplotlib-bloomberg."""

import os

from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    description = f.read()

setup(
    name="plotbb",
    version=os.environ.get("PACKAGE_VERSION", "0.2.0"),
    description="Bloomberg-inspired chart styling for Matplotlib",
    python_requires=">=3.10",
    packages=find_packages(include=["plotbb", "plotbb.*"]),
    install_requires=[
        "cycler>=0.12",
        "matplotlib>=3.11",
        "numpy>=2.0",
    ],
    long_description=description,
)
