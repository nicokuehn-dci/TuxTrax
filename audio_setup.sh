#!/bin/bash
# TuxTrax Audio Setup Script (Ubuntu/Debian)
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

MIN_JACK_VERSION=1.9.21
KX_STUDIO_REPO="https://launchpad.net/~kxstudio-debian/+archive/kxstudio"
REQUIRED_PACKAGES="ffmpeg pulseaudio libasound2-dev"

handle_error() {
    echo -e "${RED}Error: $1${NC}" >&2
    read -p "Press ENTER to exit..."
    exit 1
}

check_dependencies() {
    echo -e "${YELLOW}Checking system dependencies...${NC}"
    command -v apt-get >/dev/null 2>&1 || handle_error "This script requires apt-get package manager"
}

version_ge() { 
    test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"
}

verify_jack() {
    if command -v jackd &>/dev/null; then
        JACK_VERSION=$(jackd --version 2>&1 | grep -Po '(?<=jackd version )[\d.]+')
        if version_ge "$JACK_VERSION" "$MIN_JACK_VERSION"; then
            echo -e "${GREEN}JACK2 v$JACK_VERSION already installed${NC}"
            return 0
        else
            echo -e "${YELLOW}Found JACK2 v$JACK_VERSION (minimum v$MIN_JACK_VERSION required)${NC}"
            return 1
        fi
    else
        echo -e "${RED}JACK2 not found${NC}"
        return 1
    fi
}

install_jack() {
    echo -e "${YELLOW}Installing latest JACK2...${NC}"
    
    echo -e "${YELLOW}Adding KX Studio repositories...${NC}"
    sudo apt-get install -y apt-transport-https gpgv wget || handle_error "Failed to install repo dependencies"
    wget -q "$KX_STUDIO_REPO/+files/kxstudio-repos_11.1.0_all.deb" || handle_error "Failed to download repo package"
    sudo dpkg -i kxstudio-repos_11.1.0_all.deb || handle_error "Failed to install repo package"
    sudo apt-get update || handle_error "Failed to update package lists"

    echo -e "${YELLOW}Installing JACK2 and dependencies...${NC}"
    sudo apt-get install -y jackd2 $REQUIRED_PACKAGES || handle_error "Failed to install audio packages"
    
    if ! verify_jack; then
        handle_error "JACK2 installation failed version check"
    fi
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
    
    timeout 5 jackd -d dummy &>/dev/null &
    JACK_PID=$!
    sleep 1
    if kill -0 "$JACK_PID" 2>/dev/null; then
        echo -e "${GREEN}JACK server verified${NC}"
        kill "$JACK_PID"
    else
        handle_error "JACK server failed to start"
    fi
    
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

main() {
    check_dependencies
    if ! verify_jack; then
        install_jack
    fi
    configure_permissions
    install_tools
    post_install_check
    setup_midi_devices
    setup_recording_choices
    install_virtual_audio_cable
    
    echo -e "\n${GREEN}Audio setup completed successfully!${NC}"
    echo -e "Next steps:"
    echo -e "1. Reboot your system"
    echo -e "2. Run 'cadence' to configure your audio interface"
    echo -e "3. Start TuxTrax with './launch.py'\n"
    
    read -p "Press ENTER to exit..."
}

main
