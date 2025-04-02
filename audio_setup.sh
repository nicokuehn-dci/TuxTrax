#!/bin/bash
# TuxTrax Audio Setup Script (Ubuntu/Debian)
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

REQUIRED_PACKAGES="ffmpeg libasound2-dev pipewire pipewire-alsa libpipewire-0.3-dev portaudio19-dev libportaudio2 libportaudiocpp0 pipewire-pulse"

LOG_FILE="audio_setup.log"

log_error() {
    echo -e "${RED}Error: $1${NC}" >&2
    echo "$(date) - Error: $1" >> "$LOG_FILE"
}

log_info() {
    echo -e "${GREEN}$1${NC}"
    echo "$(date) - Info: $1" >> "$LOG_FILE"
}

handle_error() {
    log_error "$1"
    if [ "$2" == "severe" ]; then
        read -p "Press ENTER to exit..."
        exit 1
    fi
}

check_dependencies() {
    log_info "Checking system dependencies..."
    command -v apt-get >/dev/null 2>&1 || handle_error "This script requires apt-get package manager" "severe"
}

verify_pipewire() {
    if command -v pipewire &>/dev/null; then
        PIPEWIRE_VERSION=$(pipewire --version 2>&1 | grep -Po '(?<=pipewire )[\d.]+')
    fi
}

install_pipewire() {
    sudo apt-get install -y pipewire pipewire-alsa libpipewire-0.3-dev || handle_error "Failed to install PipeWire packages" "severe"
}

configure_permissions() {
    log_info "Configuring audio permissions..."
    
    if ! groups | grep -q '\baudio\b'; then
        sudo usermod -a -G audio "$USER" || handle_error "Failed to add user to audio group" "severe"
        log_info "User added to audio group - reboot required"
    fi
    
    sudo tee -a /etc/security/limits.conf <<-EOF || handle_error "Failed to configure limits" "severe"
@audio - rtprio 99
@audio - memlock unlimited
EOF

    log_info "Optimizing kernel parameters..."
    sudo tee -a /etc/sysctl.conf <<-EOF || handle_error "Failed to configure sysctl" "severe"
vm.swappiness=10
fs.inotify.max_user_watches=524288
EOF
}

install_tools() {
    read -r -p "Install optional audio tools (qjackctl, cadence)? [y/N] " -n 1
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Installing companion tools..."
        sudo apt-get install -y qjackctl cadence carla || handle_error "Failed to install tools" "severe"
    fi
}

post_install_check() {
    log_info "Running post-install checks..."
    
    log_info "Configuring PulseAudio bridge..."
    pw-cli info || handle_error "PipeWire is not running or not configured properly" "severe"
    pw-cli load-module module-alsa-source || handle_error "Failed to load module-alsa-source" "severe"
    pw-cli load-module module-alsa-sink || handle_error "Failed to load module-alsa-sink" "severe"
}

setup_midi_devices() {
    log_info "Setting up MIDI devices..."
    sudo apt-get install -y aconnectgui amidi || handle_error "Failed to install MIDI tools" "severe"
    
    log_info "Listing available MIDI devices..."
    aconnect -i -o
    amidi -l
}

setup_recording_choices() {
    log_info "Setting up recording choices..."
    sudo apt-get install -y alsa-utils || handle_error "Failed to install ALSA utilities" "severe"
    
    log_info "Configuring recording format and bitrate..."
    arecord -l
    read -p "Enter the card number for recording: " card_number
    read -p "Enter the device number for recording: " device_number
    read -p "Enter the desired format (e.g., cd, dat): " format
    read -p "Enter the desired bitrate (e.g., 16, 24): " bitrate
    
    log_info "Recording configuration: Card $card_number, Device $device_number, Format $format, Bitrate $bitrate"
    arecord -D plughw:$card_number,$device_number -f $format -r $bitrate -d 10 test_recording.wav
}

install_virtual_audio_cable() {
    log_info "Installing virtual audio cable..."
    sudo apt-get install -y zita-ajbridge || handle_error "Failed to install virtual audio cable" "severe"
}

configure_pipewire_audio_midi() {
    log_info "Configuring PipeWire for audio and MIDI..."
    pw-cli info || handle_error "PipeWire is not running or not configured properly" "severe"
    pw-cli load-module module-alsa-source || handle_error "Failed to load module-alsa-source" "severe"
    pw-cli load-module module-alsa-sink || handle_error "Failed to load module-alsa-sink" "severe"
    pw-cli load-module module-jack-source || handle_error "Failed to load module-jack-source" "severe"
    pw-cli load-module module-jack-sink || handle_error "Failed to load module-jack-sink" "severe"
    log_info "PipeWire audio and MIDI configuration complete."
}

configure_pipewire_tweaks() {
    log_info "Applying PipeWire configuration tweaks for low-latency audio..."
    sudo tee -a /etc/pipewire/pipewire.conf <<-EOF || handle_error "Failed to configure PipeWire" "severe"
# Set quantum (buffer size) for pro-audio use
default.clock.quantum = 64  # For low-latency (adjust based on your hardware)
default.clock.min-quantum = 32
default.clock.max-quantum = 1024

# Prioritize real-time scheduling
context.properties = {
    default.clock.rate = 48000
    default.clock.allowed-rates = [ 44100 48000 96000 ]
    log.level = 2  # Debug logs if needed
}
EOF
}

configure_persistent_device_routing() {
    log_info "Creating persistent device routing rules for PipeWire..."
    sudo mkdir -p /etc/pipewire/pipewire-pulse.conf.d/
    sudo tee /etc/pipewire/pipewire-pulse.conf.d/custom-rules.conf <<-EOF || handle_error "Failed to create persistent device routing rules" "severe"
# Remember device connections
context.properties = {
    default.clock.rate = 48000
    default.clock.allowed-rates = [ 44100 48000 96000 ]
    log.level = 2  # Debug logs if needed
}
EOF
}

apply_system_tweaks() {
    log_info "Applying system tweaks for RTKit priority and USB audio optimization..."
    sudo systemctl edit rtkit-daemon.service <<-EOF || handle_error "Failed to configure RTKit priority" "severe"
[Service]
LimitRTPRIO=33
LimitMEMLOCK=64M
EOF

    echo 'options snd-usb-audio nrpacks=1' | sudo tee /etc/modprobe.d/audio.conf || handle_error "Failed to configure USB audio optimization" "severe"
    sudo apt-get install -y linux-lowlatency || handle_error "Failed to install low-latency kernel" "severe"
}

install_magenta_studio() {
    log_info "Installing Magenta Studio..."
    sudo apt-get install -y magenta-studio || handle_error "Failed to install Magenta Studio" "severe"
}

main() {
    check_dependencies
    if ! verify_pipewire; then
        install_pipewire
    fi
    configure_permissions
    install_tools
    post_install_check
    setup_midi_devices
    setup_recording_choices
    install_virtual_audio_cable
    configure_pipewire_audio_midi
    configure_pipewire_tweaks
    configure_persistent_device_routing
    apply_system_tweaks
    install_magenta_studio
    
    log_info "Audio setup completed successfully!"
    log_info "Next steps:"
    log_info "1. Reboot your system"
    log_info "2. Run 'cadence' to configure your audio interface"
    log_info "3. Start TuxTrax with './launch.py'"
    
    read -p "Press ENTER to exit..."
}

main
