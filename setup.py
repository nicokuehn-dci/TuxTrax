from setuptools import setup, find_packages

setup(
    name="TuxTrax",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
            'tuxtrax=main:main',
        ],
    },
)