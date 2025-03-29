#!/bin/bash
# System dependencies
sudo apt-get update && sudo apt-get install -y \
    python3-tk \
    ffmpeg \
    jackd2 \
    libportaudio2

# Audio group config
sudo usermod -a -G audio $USER
echo "@audio - rtprio 99" | sudo tee -a /etc/security/limits.conf
echo "@audio - memlock unlimited" | sudo tee -a /etc/security/limits.conf

# Python setup
python3 -m venv daw_env
source daw_env/bin/activate
pip install -r requirements.txt
python setup.py develop