#!/bin/bash
# TuxTrax Audio Setup Script (Ubuntu/Debian)
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

REQUIRED_PACKAGES="ffmpeg pulseaudio libasound2-dev pipewire pipewire-audio-client-libraries libspa-0.2-jack pipewire-pulse"

handle_error() {
    echo -e "${RED}Error: $1${NC}" >&2
    read -p "Press ENTER to exit..."
    exit 1
}

check_dependencies() {
    echo -e "${YELLOW}Checking system dependencies...${NC}"
    command -v apt-get >/dev/null 2>&1 || handle_error "This script requires apt-get package manager"
}

verify_pipewire() {
    if command -v pipewire &>/dev/null; then
        PIPEWIRE_VERSION=$(pipewire --version 2>&1 | grep -Po '(?<=pipewire )[\d.]+')
    fi
}

install_pipewire() {
    sudo apt-get install -y pipewire pipewire-audio-client-libraries libspa-0.2-jack pipewire-pulse || handle_error "Failed to install PipeWire packages"
}

configure_permissions() {
    echo -e "${YELLOW}Configuring audio permissions...${NC}"
    
    if ! groups | grep -q '\baudio\b'; then
        sudo usermod -a -G audio "$USER" || handle_error "Failed to add user to audio group"
        echo -e "${GREEN}User added to audio group - reboot required${NC}"
    fi
    
    sudo tee -a /etc/security/limits.conf <<-EOF || handle_error "Failed to configure limits"
@audio - rtprio 99
@audio - memlock unlimited
EOF

    echo -e "${YELLOW}Optimizing kernel parameters...${NC}"
    sudo tee -a /etc/sysctl.conf <<-EOF || handle_error "Failed to configure sysctl"
vm.swappiness=10
fs.inotify.max_user_watches=524288
EOF
}

install_tools() {
    read -r -p "Install optional audio tools (qjackctl, cadence)? [y/N] " -n 1
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Installing companion tools...${NC}"
        sudo apt-get install -y qjackctl cadence carla || handle_error "Failed to install tools"
    fi
}

post_install_check() {
    echo -e "${YELLOW}Running post-install checks...${NC}"
    
    echo -e "${YELLOW}Configuring PulseAudio bridge...${NC}"
    pactl load-module module-jack-sink >/dev/null || handle_error "Failed to load JACK sink"
    pactl load-module module-jack-source >/dev/null || handle_error "Failed to load JACK source"
}

setup_midi_devices() {
    echo -e "${YELLOW}Setting up MIDI devices...${NC}"
    sudo apt-get install -y aconnectgui amidi || handle_error "Failed to install MIDI tools"
    
    echo -e "${YELLOW}Listing available MIDI devices...${NC}"
    aconnect -i -o
    amidi -l
}

setup_recording_choices() {
    echo -e "${YELLOW}Setting up recording choices...${NC}"
    sudo apt-get install -y alsa-utils || handle_error "Failed to install ALSA utilities"
    
    echo -e "${YELLOW}Configuring recording format and bitrate...${NC}"
    arecord -l
    read -p "Enter the card number for recording: " card_number
    read -p "Enter the device number for recording: " device_number
    read -p "Enter the desired format (e.g., cd, dat): " format
    read -p "Enter the desired bitrate (e.g., 16, 24): " bitrate
    
    echo -e "${YELLOW}Recording configuration: Card $card_number, Device $device_number, Format $format, Bitrate $bitrate${NC}"
    arecord -D plughw:$card_number,$device_number -f $format -r $bitrate -d 10 test_recording.wav
}

install_virtual_audio_cable() {
    echo -e "${YELLOW}Installing virtual audio cable...${NC}"
    sudo apt-get install -y zita-ajbridge || handle_error "Failed to install virtual audio cable"
}

configure_pipewire_audio_midi() {
    echo -e "${YELLOW}Configuring PipeWire for audio and MIDI...${NC}"
    pw-cli info || handle_error "PipeWire is not running or not configured properly"
    pw-cli load-module module-alsa-source || handle_error "Failed to load module-alsa-source"
    pw-cli load-module module-alsa-sink || handle_error "Failed to load module-alsa-sink"
    pw-cli load-module module-jack-source || handle_error "Failed to load module-jack-source"
    pw-cli load-module module-jack-sink || handle_error "Failed to load module-jack-sink"
    echo -e "${GREEN}PipeWire audio and MIDI configuration complete.${NC}"
}

configure_pipewire_tweaks() {
    echo -e "${YELLOW}Applying PipeWire configuration tweaks for low-latency audio...${NC}"
    sudo tee -a /etc/pipewire/pipewire.conf <<-EOF || handle_error "Failed to configure PipeWire"
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
    echo -e "${YELLOW}Creating persistent device routing rules for PipeWire...${NC}"
    sudo mkdir -p /etc/pipewire/pipewire-pulse.conf.d/
    sudo tee /etc/pipewire/pipewire-pulse.conf.d/custom-rules.conf <<-EOF || handle_error "Failed to create persistent device routing rules"
# Remember device connections
context.properties = {
    default.clock.rate = 48000
    default.clock.allowed-rates = [ 44100 48000 96000 ]
    log.level = 2  # Debug logs if needed
}
EOF
}

apply_system_tweaks() {
    echo -e "${YELLOW}Applying system tweaks for RTKit priority and USB audio optimization...${NC}"
    sudo systemctl edit rtkit-daemon.service <<-EOF || handle_error "Failed to configure RTKit priority"
[Service]
LimitRTPRIO=33
LimitMEMLOCK=64M
EOF

    echo 'options snd-usb-audio nrpacks=1' | sudo tee /etc/modprobe.d/audio.conf || handle_error "Failed to configure USB audio optimization"
    sudo apt-get install -y linux-lowlatency || handle_error "Failed to install low-latency kernel"
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
    
    echo -e "\n${GREEN}Audio setup completed successfully!${NC}"
    echo -e "Next steps:"
    echo -e "1. Reboot your system"
    echo -e "2. Run 'cadence' to configure your audio interface"
    echo -e "3. Start TuxTrax with './launch.py'\n"
    
    read -p "Press ENTER to exit..."
}

main
