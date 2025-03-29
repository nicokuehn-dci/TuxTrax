import sounddevice as sd
import numpy as np
from threading import Lock
from pedalboard import Pedalboard

class AudioEngine:
    def __init__(self, sr=48000, buffer_size=512):
        self.sr = sr
        self.buffer_size = buffer_size
        self.mix_buffer = np.zeros((buffer_size, 2), dtype=np.float32)
        self.lock = Lock()
        self.fx_rack = Pedalboard()
        
        self.stream = sd.OutputStream(
            samplerate=sr,
            blocksize=buffer_size,
            callback=self._callback,
            dtype='float32'
        )

    def _callback(self, outdata, frames, time, status):
        with self.lock:
            processed = self.fx_rack.process(self.mix_buffer, self.sr)
            outdata[:] = processed
            self.mix_buffer.fill(0)

    def add_audio(self, audio):
        with self.lock:
            end = min(len(audio), self.buffer_size)
            self.mix_buffer[:end] += audio[:end]

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()