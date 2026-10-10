import numpy as np
import random
import time
def generate_sine_waveform(frequency, sample_rate, duration, intensity = 16000):
    # say we had a frequency of 100hz therefore we need to 
    # loop a sine every rate / freq samples = period
    n_samples = int(sample_rate * duration)
    samples = np.array([
        intensity * np.sin(2 * np.pi * frequency * n / sample_rate)
        for n in range(n_samples)
    ])
    return samples.astype(np.int16)


def generate_complex(freqs, sample_rate, duration, intensity = 16000, rando = False):
    random.seed(time.time())
    combined = np.sum(
        [generate_sine_waveform(f, sample_rate, duration,
                                 intensity // 10 * random.randint(2, 20) if rando else intensity)
         for f in freqs],
        axis=0
    )
    
    peak = np.max(np.abs(combined))
    if peak > 32767:
        combined = combined / peak * 32767
    return combined.astype(np.int16)