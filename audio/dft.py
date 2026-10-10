#dft
import numpy as np
from numpy import complex128 as complex
import math
import matplotlib.pyplot as plt
from itertools import accumulate
import ctypes
import time
from enum import Enum

import scipy.io.wavfile as wav

#constants
e = complex(math.e)
pi = complex(math.pi)

class DFT(Enum):
    DFT = 1
    FFT = 0
    NOT_IMPL = 3

class WINDOW(Enum):
    NOWINDOW = 0
    HANNING = 1
    NOT_IMPL = 3


def dft_factory(type: DFT):
    match type:
        case DFT.DFT:
            return getDFT
        case DFT.FFT:
            return np.fft.fft


def getSingleDFT(sample: np.array, k: complex) -> complex:
    n = len(sample)
    indices = np.arange(n)
    return np.sum(sample * np.exp(-1j * 2 * np.pi * k * indices / n))
    

def getDFT(sample: np.array) -> np.array:
    result = np.array([],dtype=complex)
    for k in range(0,len(sample)):
        Xk = getSingleDFT(sample, k)
        result = np.append(result, Xk)
    return result

def getSTFT(sample ,sample_rate, window_ms, useDFT):
    stft_matrix = []
    dft = getDFT if useDFT else np.fft.fft
    window_size = int(window_ms / 1000 * sample_rate)

    for start in range(0,len(sample), window_size):
        end = start + window_size
        window = sample[start:end]
        if (len(window) != window_size):
            window = np.pad(window, (0, window_size - len(window)))
        spectrum = dft(window)
        spectrum = spectrum[:window_size // 2 + 1]
        stft_matrix.append(spectrum)
        
    
    return stft_matrix

def plot_spectrum(result, sample_rate):
    n = len(result)
    print(n)
    magnitudes = np.abs(result)
    
    freqs = np.fft.fftfreq(n, d=1/sample_rate)
    half = n // 2
    print(freqs[100])
    
    plt.figure(figsize=(12, 4))
    plt.plot(freqs[:half], magnitudes[:half])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Spectrum")
    plt.xlim(0, 20000)
    plt.grid(True)
    plt.savefig("spectrum.png", dpi=150)
    plt.show()

# 
# if samples.ndim == 2:
#     samples = samples.mean(axis=1).astype(samples.dtype)

# duration = len(samples) / 44100

# print(f"clip of {duration} seconds, rate of {sample_rate} and {len(samples)} samples using {len(samples)**2 * 16 / 1000000000} gb of memory")

# stft_matrix = getSTFT(samples, 44100, 50, False)

# plottable = [[abs(x) for x in row] for row in stft_matrix]

# lenToPad = len(plottable[0])
# plottable[-1] = np.pad(plottable[-1], (0, lenToPad - len(plottable[-1])))

# duration = len(samples) / 44100

# magnitude = np.abs(plottable).T

# image = 20 * np.log10(magnitude + 1e-12)
# image -= image.max()          
# image = np.maximum(image, -80)

# plt.imshow(
#     image,
#     cmap="magma",
#     origin="lower",
#     aspect="auto",
#     extent=[0, duration, 0, sample_rate / 2]
# )

# plt.xlabel("Time (s)")
# plt.ylabel("Frequency (Hz)")
# plt.colorbar(label="Log Magnitude")
# plt.show()