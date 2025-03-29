#!/bin/bash

set -e  # Exit immediately on error
set -u  # Treat unset variables as errors

APP_NAME="TuxTrax"
REPO_URL="https://github.com/nicokuehn-dci/TuxTrax"
PYTHON_VERSION="3.10"
VENV_NAME=".venv"
DIRS=("gui" "mixer" "player" "sampler" "storage" "tests")

echo "🔧 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing required packages..."
sudo apt install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev \
                     build-essential libjack-jackd2-dev jackd2 qtbase5-dev \
                     libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 \
                     ffmpeg git curl

# Set up JACK audio permissions
echo "🔊 Configuring JACK for real-time performance..."
if ! grep -q "@audio - rtprio 95" /etc/security/limits.conf; then
    echo "@audio - rtprio 95" | sudo tee -a /etc/security/limits.conf
    echo "@audio - memlock unlimited" | sudo tee -a /etc/security/limits.conf
    echo "⚠️ Please log out and log back in to apply JACK audio group settings."
fi

# Clone repo
if [ ! -d "$APP_NAME" ]; then
    echo "📁 Cloning $APP_NAME repository..."
    git clone "$REPO_URL"
else
    echo "📁 Repository already cloned. Pulling latest changes..."
    cd "$APP_NAME"
    git pull
    cd ..
fi

cd "$APP_NAME"

# Create folders based on modular structure
echo "📂 Creating module directories..."
for d in "${DIRS[@]}"; do
    mkdir -p "src/$d"
done

# Create and activate virtual environment
echo "🐍 Setting up Python $PYTHON_VERSION virtual environment..."
python$PYTHON_VERSION -m venv $VENV_NAME
source $VENV_NAME/bin/activate

# Create requirements.txt
echo "🧾 Writing requirements.txt..."
cat > requirements.txt <<EOF
numpy==1.24.4
soundfile
pedalboard>=0.8.2
pyaudio
PyQt5
pyqtgraph
EOF

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

sudo apt install -y pipewire pipewire-audio-client-libraries libspa-0.2-jack pipewire-pulse
# PipeWire automatically handles sink/source routing; no need for manual pactl commands.


# Configure PulseAudio bridge
echo "🔧 Configuring PulseAudio bridge..."
pactl load-module module-jack-sink
pactl load-module module-jack-source

echo "✅ Installation complete!"
echo ""
echo "🚀 To run TuxTrax:"
echo "----------------------------------------"
echo "cd $APP_NAME"
echo "source $VENV_NAME/bin/activate"
echo "python3 src/main.py"
echo "----------------------------------------"
