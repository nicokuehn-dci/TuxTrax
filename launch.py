#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Configuration
VENV_NAME = "daw_env"
REQUIREMENTS_FILE = "requirements.txt"
PYTHON_CMD = "python3" if platform.system() != "Windows" else "python"
MIN_JACK_VERSION = (1, 9, 21)
REQUIRED_BINARIES = ['jackd', 'ffmpeg', 'pulseaudio']

def print_header():
    print(r"""
    ████████╗██╗  ██╗███████╗████████╗████████╗██████╗  █████╗ ██╗  ██╗
    ╚══██╔══╝██║  ██║██╔════╝╚══██╔══╝╚══██╔══╝██╔══██╗██╔══██╗╚██╗██╔╝
       ██║   ███████║█████╗     ██║      ██║   ██████╔╝███████║ ╚███╔╝ 
       ██║   ██╔══██║██╔══╝     ██║      ██║   ██╔══██╗██╔══██║ ██╔██╗ 
       ██║   ██║  ██║███████╗   ██║      ██║   ██║  ██║██║  ██║██╔╝ ██╗
       ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    """)

def check_venv():
    venv_path = Path(VENV_NAME)
    return (venv_path / "bin" / "activate").exists()

def check_audio_group():
    groups = subprocess.check_output(['groups']).decode().split()
    return 'audio' in groups

def check_jack_version():
    try:
        output = subprocess.check_output(['jackd', '-v'], stderr=subprocess.STDOUT)
        version_str = output.decode().split()[2].strip('v')
        version = tuple(map(int, version_str.split('.')))
        return version >= MIN_JACK_VERSION
    except Exception:
        return False

def check_system_deps():
    missing = []
    for bin in REQUIRED_BINARIES:
        if not shutil.which(bin):
            missing.append(bin)
    return missing

def setup_jack_config():
    jackdrc = Path.home() / '.jackdrc'
    if not jackdrc.exists():
        with open(jackdrc, 'w') as f:
            f.write("jackd -d alsa -r 48000 -p 256 -n 2")

def configure_pulse_jack():
    subprocess.run(['pactl', 'load-module', 'module-jack-sink'], check=True)
    subprocess.run(['pactl', 'load-module', 'module-jack-source'], check=True)
    subprocess.run(['pacmd', 'set-default-sink', 'jack_out'], check=True)

def setup_environment():
    print("⚙️ Setting up environment...")
    try:
        subprocess.run([PYTHON_CMD, "-m", "venv", VENV_NAME], check=True)
        pip_path = str(Path(VENV_NAME)) / "bin" / "pip"
        subprocess.run([pip_path, "install", "-r", REQUIREMENTS_FILE], check=True)
        subprocess.run([pip_path, "install", "-e", "."], check=True)
        print("✅ Environment setup complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False

def launch_app():
    print("🚀 Launching TuxTrax...")
    try:
        python_path = str(Path(VENV_NAME)) / "bin" / "python"
        subprocess.run([python_path, "-m", "tuxtrax"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Session terminated")

def system_check():
    print("🔍 Running system checks...")
    issues = []
    
    if not check_audio_group():
        issues.append("User not in 'audio' group - run:\n  sudo usermod -a -G audio $USER && reboot")
    
    if not check_jack_version():
        issues.append(f"JACK2 >= {'.'.join(map(str, MIN_JACK_VERSION))} required")
    
    if missing := check_system_deps():
        issues.append(f"Missing binaries: {', '.join(missing)}\n  sudo apt install jackd2 ffmpeg pulseaudio")
    
    if issues:
        print("\n❌ System configuration issues:")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        return False
    
    try:
        setup_jack_config()
        configure_pulse_jack()
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Audio config failed: {e}")
        return False

def main():
    print_header()
    
    if not system_check():
        sys.exit(1)
    
    if not check_venv():
        print("🛠️ Virtual environment missing")
        if input("Setup environment? [Y/n]: ").lower() != 'n':
            if not setup_environment():
                sys.exit(1)
        else:
            print("❌ Setup aborted")
            sys.exit(1)
    
    launch_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        sys.exit(0)