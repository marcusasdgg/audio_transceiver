from enum import Enum

import audio.dft as dft 
import scipy.io.wavfile as wav
import numpy as np

import matplotlib.pyplot as plt

class DFT(Enum):
    DFT = 1
    FFT = 0
    NOT_IMPL = 3

class WINDOW(Enum):
    NOWINDOW = 0
    HANNING = 1
    NOT_IMPL = 3


# lazy type which calculates stft on the fly?  
# class fields: 
#   - stft: a 2d matrix of which x is the time domain, y is the frequency domain
#   - dft: underlying function for the base dft

#
num= 0


class spectrogram:
    def __init__(self, path: str, resolution: int, dft_type: DFT,  window_type: WINDOW) -> None:
        if (path is not str):
            self.sample_rate = 44100
            self.samples = path
        else:
            sample_rate, samples = wav.read(path)
            self.sample_rate = sample_rate
            self.samples = samples.mean(axis=1).astype(samples.dtype)
        
        self.resolution = resolution
        self.dft_type = dft_type
        self.window_type = window_type
        self.window_size = int(self.resolution / 1000 * self.sample_rate)
        return



    def trigger_stft(self):
        self.stft = dft.getSTFT(self.samples, self.sample_rate, self.resolution, self.dft_type)

    # gets a 3d array of magnitudes
    # x dim is time y dim is frequency and value is magnitude
    def get_spectrogram(self) -> np.matrix:
        if not hasattr(self, "stft"):
            self.trigger_stft()

        mag_vec = (np.abs(self.stft) / self.window_size).T
        return mag_vec

    def display_spectrogram(self):
        global num
        data = self.get_spectrogram()
        db = 20 * np.log10(data + 1e-12)
        plt.figure(num)
        num += 1
        plt.imshow(
            db,
            origin="lower",
            aspect="auto",
            extent=[
                0,
                len(self.samples) / self.sample_rate,
                0,
                self.sample_rate / 2,
            ],
            vmin = 0,
            vmax = 80,
            cmap="magma",
        )

        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")

    def show(self):
        plt.show()

        
                
        

        

# ambatugram = spectrogram(r"Ambatukam Dreamy Bull Sound Effect.wav", 50, 1, 0)
# ambatugram2 = spectrogram(r"Ambatukam Dreamy Bull Sound Effect.wav", 50, 0, 0)
# print(f"dft and np.fft are {"equivalent" if np.allclose(ambatugram.get_spectrogram(), ambatugram2.get_spectrogram()) else "not equivalent"} ")

# ambatugram.display_spectrogram()
# ambatugram2.display_spectrogram()
# plt.show()