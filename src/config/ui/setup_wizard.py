from PyQt5.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QPushButton
from .dialogs.device_config import AudioDeviceDialog
from ..config.settings import AudioMIDISettings
import subprocess
import pyudev
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

class SetupWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.settings = AudioMIDISettings()
        self.setWindowTitle("TuxTrax Initial Setup")
        self.addPage(AudioDevicePage())
        self.addPage(AudioRoutingPage())
        self.addPage(DeviceHotplugPage())

class AudioDevicePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.ui = AudioDeviceDialog()
        layout = QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)
        
    def save_settings(self):
        self.settings.config['Audio']['buffersize'] = str(self.ui.buffer_spin.value())
        self.settings.save()

class AudioRoutingPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Audio Routing")
        self.setSubTitle("Configure your audio routing using Helvum.")
        
        layout = QVBoxLayout()
        self.helvum_button = QPushButton("Launch Helvum")
        self.helvum_button.clicked.connect(self.launch_helvum)
        layout.addWidget(self.helvum_button)
        self.setLayout(layout)
        
    def launch_helvum(self):
        try:
            subprocess.run(['helvum'], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error launching Helvum: {e}")
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")

class DeviceHotplugPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Device Hotplug")
        self.setSubTitle("Monitor and configure hot-plugged devices.")
        
        layout = QVBoxLayout()
        self.monitor_button = QPushButton("Start Monitoring")
        self.monitor_button.clicked.connect(self.start_monitoring)
        layout.addWidget(self.monitor_button)
        self.setLayout(layout)
        
    def start_monitoring(self):
        try:
            context = pyudev.Context()
            monitor = pyudev.Monitor.from_netlink(context)
            monitor.filter_by(subsystem='usb')
            observer = pyudev.MonitorObserver(monitor, self.device_event)
            observer.start()
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
        
    def device_event(self, action, device):
        try:
            logger.info(f"Device {action}: {device}")
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
