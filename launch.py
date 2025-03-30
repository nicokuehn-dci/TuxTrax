#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil
import argparse
import logging
from pathlib import Path

# Configuration
PYTHON_CMD = "python3" if platform.system() != "Windows" else "python"
REQUIRED_BINARIES = ['pw-cli', 'ffmpeg', 'pulseaudio', 'aconnect', 'amidi', 'arecord']

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def print_header():
    print(r"""
    ████████╗██╗  ██╗███████╗████████╗████████╗██████╗  █████╗ ██╗  ██╗
    ╚══██╔══╝██║  ██║██╔════╝╚══██╔══╝╚══██╔══╝██╔══██╗██╔══██╗╚██╗██╔╝
       ██║   ███████║█████╗     ██║      ██║   ██████╔╝███████║ ╚███╔╝ 
       ██║   ██╔══██║██╔══╝     ██║      ██║   ██╔══██╗██╔══██║ ██╔██╗ 
       ██║   ██║  ██║███████╗   ██║      ██║   ██║  ██║██║  ██║██╔╝ ██╗
       ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    """)

def check_audio_group():
    try:
        groups = subprocess.check_output(['groups']).decode().split()
        return 'audio' in groups
    except Exception as e:
        logger.error(f"Error checking audio group: {e}")
        return False

def check_pipewire_version():
    output = subprocess.check_output(['pipewire', '--version'], stderr=subprocess.STDOUT)
    version_str = output.decode().split()[1]
    version = tuple(map(int, version_str.split('.')))
    return version >= (0, 3, 50)

def check_pipewire_configuration():
    try:
        subprocess.run(['pw-cli', 'info'], check=True)
        logger.info("PipeWire is configured and running.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking PipeWire configuration: {e}")
        return False

def check_system_deps():
    missing = []
    for bin in REQUIRED_BINARIES:
        if not shutil.which(bin):
            missing.append(bin)
    return missing

def configure_pipewire():
    try:
        subprocess.run(['pw-cli', 'info'], check=True)
        logger.info("PipeWire is configured and running.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error configuring PipeWire: {e}")
        raise

def configure_pipewire_audio_midi():
    try:
        logger.info("🔧 Configuring PipeWire for audio and MIDI...")
        subprocess.run(['pw-cli', 'info'], check=True)
        subprocess.run(['pw-cli', 'load-module', 'module-alsa-source'], check=True)
        subprocess.run(['pw-cli', 'load-module', 'module-alsa-sink'], check=True)
        subprocess.run(['pw-cli', 'load-module', 'module-jack-source'], check=True)
        subprocess.run(['pw-cli', 'load-module', 'module-jack-sink'], check=True)
        logger.info("PipeWire audio and MIDI configuration complete.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error configuring PipeWire for audio and MIDI: {e}")
        raise

def setup_midi_devices():
    try:
        logger.info("🔧 Setting up MIDI devices...")
        subprocess.run(['aconnect', '-i', '-o'], check=True)
        subprocess.run(['amidi', '-l'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting up MIDI devices: {e}")
        raise

def setup_recording_choices():
    try:
        logger.info("🔧 Setting up recording choices...")
        subprocess.run(['arecord', '-l'], check=True)
        
        while True:
            card_number = input("Enter the card number for recording: ")
            device_number = input("Enter the device number for recording: ")
            format = input("Enter the desired format (e.g., cd, dat): ")
            bitrate = input("Enter the desired bitrate (e.g., 16, 24): ")

            if card_number.isdigit() and device_number.isdigit() and bitrate.isdigit():
                break
            else:
                logger.error("Invalid input. Please enter numeric values for card/device/bitrate.")

        logger.info(f"Recording configuration: Card {card_number}, Device {device_number}, Format {format}, Bitrate {bitrate}")
        
        subprocess.run(
            ['arecord', '-D', f'plughw:{card_number},{device_number}', '-f', format, '-r', bitrate, '-d', '10', 'test_recording.wav'],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting up recording choices: {e}")
        raise

def setup_multitrack_recording():
    logger.info("🔧 Setting up multi-track recording...")
    # Add any necessary configuration or setup for multi-track recording here

def launch_app():
    try:
        logger.info("🚀 Launching TuxTrax...")
        subprocess.run(["tuxtrax"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to launch TuxTrax: {e}")
    except KeyboardInterrupt:
        logger.info("\n🛑 Session terminated")

def system_check():
    logger.info("🔍 Running system checks...")
    issues = []
    
    if not check_audio_group():
        issues.append("User not in 'audio' group - run:\n  sudo usermod -a -G audio $USER && reboot")
    
    if not check_pipewire_version():
        issues.append(f"PipeWire >= 0.3.50 required")
    
    if not check_pipewire_configuration():
        issues.append("PipeWire is not properly configured")
    
    if missing := check_system_deps():
        issues.append(f"Missing binaries: {', '.join(missing)}\n  sudo apt install pipewire ffmpeg pulseaudio aconnect amidi arecord")
    
    if issues:
        logger.error("\n❌ System configuration issues:")
        for i, issue in enumerate(issues, 1):
            logger.error(f"{i}. {issue}")
        return False
    
    return True

def parse_args():
    parser = argparse.ArgumentParser(description="Launch TuxTrax with system checks and configuration.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Set logging level based on debug flag
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    print_header()
    
    # Run system checks before proceeding
    if not system_check():
        sys.exit(1)

    # Perform configurations after successful system checks
    try:
        configure_pipewire()
        configure_pipewire_audio_midi()
        setup_midi_devices()
        setup_recording_choices()
        setup_multitrack_recording()
        
        # Launch application after all configurations are complete
        launch_app()
        
    except Exception as e:
        logger.error(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n🛑 Operation cancelled")
