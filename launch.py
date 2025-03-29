#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Configuration
# VENV_NAME = "daw_env" # Removed
# REQUIREMENTS_FILE = "requirements.txt" # Removed
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

# def check_venv(): # Removed
#     venv_path = Path(VENV_NAME)
#     return (venv_path / "bin" / "activate").exists() # Removed

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

# def setup_environment(): # Removed
#     print("⚙️ Setting up environment...") # Removed
#     try: # Removed
#         subprocess.run([PYTHON_CMD, "-m", "venv", VENV_NAME], check=True) # Removed
#         pip_path = str(Path(VENV_NAME)) / "bin" / "pip" # Removed
#         subprocess.run([pip_path, "install", "-r", REQUIREMENTS_FILE], check=True) # Removed
#         subprocess.run([pip_path, "install", "-e", "."], check=True) # Removed
#         print("✅ Environment setup complete!") # Removed
#         return True # Removed
#     except subprocess.CalledProcessError as e: # Removed
#         print(f"❌ Setup failed: {e}") # Removed
#         return False # Removed

def launch_app():
    print("🚀 Launching TuxTrax...")
    try:
        # python_path = str(Path(VENV_NAME)) / "bin" / "python" # Removed
        # subprocess.run([python_path, "-m", "tuxtrax"], check=True) # Removed
        subprocess.run(["tuxtrax"], check=True) # Changed
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
    
    # if not check_venv(): # Removed
    #     print("🛠️ Virtual environment missing") # Removed
    #     if input("Setup environment? [Y/n]: ").lower() != 'n': # Removed
    #         if not setup_environment(): # Removed
    #             sys.exit(1) # Removed
    #     else: # Removed
    #         print("❌ Setup aborted") # Removed
    #         sys.exit(1) # Removed
    
    launch_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled")
        sys.exit(0)
