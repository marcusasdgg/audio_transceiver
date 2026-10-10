import threading

import audio.dft as dft
from audio.dft import DFT
import numpy as np
import scipy.io.wavfile as wav


# what cutoff type should we use?
# take top n * 2 loudest frequencies?

class freq_analyser:
    # window and dft selector
    dft_type = DFT.FFT
    def __init__(self, frequencies, cuttoff, sample_rate):
        self.dft = dft.dft_factory(self.dft_type)
        self.cutoff = cuttoff
        self.frequencies = set(frequencies)
        self.sample_rate = sample_rate

    def set_cutoff(self,cutoff):
        self.cutoff = cutoff

    # calls handler whose arguments are a single list of frequencies which we will feed our found frequencies
    def add_hook(self, stream, handler, chunk_len):
        self.handler = handler
        self.stream = stream
        self.chunk_len = chunk_len

    def handle_event(self):
        while self.run == True:
            chunk = self.stream.read(self.chunk_len)
            arr = np.frombuffer(chunk, dtype=np.int16)
            self.handler(self.search_sample(arr))

    def release_hook(self):
        self.run = False
        self.thread.join()
        return

    def start(self):
        self.stream.start_stream()
        self.run = True
        self.thread = threading.Thread(target=self.handle_event)
        self.thread.start()
        return

    def search_sample(self, samples: np.array) -> set : 
        n = len(samples)
        freqs = np.fft.fftfreq(n, d=1/self.sample_rate)
        freqs = freqs[:n//2]

        fourier = self.dft(samples)
        magnitudes = np.abs(fourier[:n//2]) / (n/2)
        res = set()

        for i in self.frequencies:
            bin_index = int(round(i * n / self.sample_rate))
            if bin_index < len(magnitudes) and magnitudes[bin_index] > self.cutoff:
                res.add(i)

    
        return res




    


