import mido
from mido import Message
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MidiHandler:
    def __init__(self):
        self.input_ports = mido.get_input_names()
        self.output_ports = mido.get_output_names()
        self.active_input = None
        self.active_output = None

    def send_midi_note(self, note, velocity=64, channel=0):
        try:
            msg = Message('note_on', note=note, velocity=velocity, channel=channel)
            self._send_message(msg)
        except Exception as e:
            logger.error(f"Error sending MIDI note: {e}")

    def send_cc(self, control, value, channel=0):
        try:
            msg = Message('control_change', control=control, value=value, channel=channel)
            self._send_message(msg)
        except Exception as e:
            logger.error(f"Error sending MIDI control change: {e}")

    def _send_message(self, msg):
        if self.active_output:
            try:
                with mido.open_output(self.active_output) as outport:
                    outport.send(msg)
            except Exception as e:
                logger.error(f"Error sending MIDI message: {e}")

    def receive_midi(self):
        if self.active_input:
            try:
                with mido.open_input(self.active_input) as inport:
                    for msg in inport:
                        print(f"Received message: {msg}")
            except Exception as e:
                logger.error(f"Error receiving MIDI message: {e}")
