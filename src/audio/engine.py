import sounddevice as sd
import numpy as np
from threading import Lock
from pedalboard import Pedalboard
import pipewire as pw

class AudioEngine:
    def __init__(self, sr=48000, buffer_size=512):
        self.sr = sr
        self.buffer_size = buffer_size
        self.mix_buffer = np.zeros((buffer_size, 2), dtype=np.float32)
        self.lock = Lock()
        self.fx_rack = Pedalboard()
        
        pw.init(None, None)
        self.context = pw.Context()
        self.core = self.context.connect()
        
        self.stream = pw.Stream(self.core, "TuxTrax-Audio", None)
        self.stream.add_listener(self._stream_listener)
        self.stream.connect(pw.DIRECTION_INPUT, pw.ID_ANY, pw.STREAM_FLAG_AUTOCONNECT, None, 0)

    def _stream_listener(self, stream, buffer):
        with self.lock:
            processed = self.fx_rack.process(self.mix_buffer, self.sr)
            buffer[:] = processed
            self.mix_buffer.fill(0)

    def add_audio(self, audio):
        with self.lock:
            end = min(len(audio), self.buffer_size)
            self.mix_buffer[:end] += audio[:end]

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def set_latency(self, latency_ms):
        """Set the desired latency for the audio engine."""
        self.stream.set_latency(latency_ms)

    def get_latency(self):
        """Get the current latency of the audio engine."""
        return self.stream.get_latency()

    def monitor_latency(self):
        """Monitor the latency of the audio engine."""
        latency = self.get_latency()
        print(f"Current latency: {latency} ms")
