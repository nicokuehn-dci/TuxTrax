import mido
from mido import Message

class MidiHandler:
    def __init__(self):
        self.input_ports = mido.get_input_names()
        self.output_ports = mido.get_output_names()
        self.active_input = None
        self.active_output = None

    def send_midi_note(self, note, velocity=64, channel=0):
        msg = Message('note_on', note=note, velocity=velocity, channel=channel)
        self._send_message(msg)

    def send_cc(self, control, value, channel=0):
        msg = Message('control_change', control=control, value=value, channel=channel)
        self._send_message(msg)

    def _send_message(self, msg):
        if self.active_output:
            with mido.open_output(self.active_output) as outport:
                outport.send(msg)

    def receive_midi(self):
        if self.active_input:
            with mido.open_input(self.active_input) as inport:
                for msg in inport:
                    print(f"Received message: {msg}")
