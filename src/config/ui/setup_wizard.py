from PyQt5.QtWidgets import QWizard, QWizardPage, QVBoxLayout, QPushButton
from .dialogs.device_config import AudioDeviceDialog
from ..config.settings import AudioMIDISettings
import subprocess
import ctypes
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
            libudev = ctypes.CDLL('libudev.so.1')
            context = libudev.udev_new()
            monitor = libudev.udev_monitor_new_from_netlink(context, b'udev')
            libudev.udev_monitor_filter_add_match_subsystem_devtype(monitor, b'usb', None)
            libudev.udev_monitor_enable_receiving(monitor)
            fd = libudev.udev_monitor_get_fd(monitor)
            
            while True:
                rlist, _, _ = select.select([fd], [], [], 1)
                if fd in rlist:
                    device = libudev.udev_monitor_receive_device(monitor)
                    action = libudev.udev_device_get_action(device)
                    self.device_event(action, device)
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
        
    def device_event(self, action, device):
        try:
            logger.info(f"Device {action}: {device}")
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
