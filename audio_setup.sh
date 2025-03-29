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
        if version_ge $JACK_VERSION $MIN_JACK_VERSION; then
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
    wget -q $KX_STUDIO_REPO/+files/kxstudio-repos_11.1.0_all.deb || handle_error "Failed to download repo package"
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
        sudo usermod -a -G audio $USER || handle_error "Failed to add user to audio group"
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
    read -p "Install optional audio tools (qjackctl, cadence)? [y/N] " -n 1
