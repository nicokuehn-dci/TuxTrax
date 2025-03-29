from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="TuxTrax",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # Tell setuptools that packages are under the 'src' directory
    install_requires=[
        # Keep only Python dependencies
        'numpy>=1.26',
        'PyQt5>=5.15',
        'pedalboard>=0.7',
        'librosa>=0.10',
        'sounddevice>=0.4',
        'mido>=1.2',
        'python-rtmidi>=1.5',
        'pyqtgraph>=0.13',
        'PyYAML>=6.0',
        'soundfile>=0.12'
    ],
    entry_points={
        'console_scripts': [
            'tuxtrax=main:MainWindow', # Changed entry point
        ],
    },
    package_data={
        '': ['*.yaml'],  # Include any .yaml files in the package
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
