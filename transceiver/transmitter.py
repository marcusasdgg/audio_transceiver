
# generates pure sine tones at given frequency set to generate a byte
import numpy as np
import pyaudio
from .helpers import find_first_dev
from audio.synthesis import generate_sine_waveform, generate_complex

class transmitter:

    def __init__(self, sample_length_ms, output_name, symbols):
        p = pyaudio.PyAudio()

        index, dev = find_first_dev(p,output_name)
        self.sample_rate = int(dev["defaultSampleRate"])
        self.start = symbols["start"]
        self.end = symbols["end"]
        self.data_sy = list(reversed(symbols["data"]))
        self.length = sample_length_ms / 1000


        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            output_device_index=index,
            output=True
        )

    def transmit_data(self, data, mult):
        # send our data synchrously for now
        # construct our start signal
        start = generate_sine_waveform(self.start, self.sample_rate,self.length)
        end = generate_sine_waveform(self.end, self.sample_rate,self.length)

        # get individaul bits of data
        freqs = [item * (data & (0b1 << i) != 0) for (i,item) in enumerate(self.data_sy)]
        freqs = generate_complex(freqs, self.sample_rate, mult * self.length)
        
        # play our start, freqs end in order
        self.stream.write(start)
        self.stream.write(freqs)
        self.stream.write(end)
        return 


