import sys
from setuptools import setup, find_packages

# Base dependencies
install_requires = [
    # "docker",
    # "pysingularity",
    "pyyaml",
    "psutil",
    "nvidia-ml-py3",
    "pyroute2",
    "loguru",
    "click",
    "python-dotenv",
    "pytest"
]

# Add NUMA only on Linux
if sys.platform.startswith("linux"):
    install_requires.append("numa")

setup(
    name="PyRune",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=install_requires,
    python_requires=">=3.10",
)