import threading

from transceiver.receiver import receiver
from transceiver.transmitter import transmitter
import numpy as np
import time
import pyaudio
from audio.dft import getDFT, plot_spectrum
from audio.synthesis import generate_complex, generate_sine_waveform
from audio.spectrogram import spectrogram

def spectrum_snapshot():
    tx = transmitter(0,"2nd output",{"start": 200, "end": 1100, "data": [1000,900,800,700,600,500,400,300]} )
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = int(RATE * 0.050)
    DEVICE_INDEX = 1

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=DEVICE_INDEX,
        frames_per_buffer=CHUNK,
    )

    frames = []
    recording = threading.Event()
    recording.set()

    def _record_loop():
        while recording.is_set():
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

    record_thread = threading.Thread(target=_record_loop, daemon=True)
    record_thread.start()

    start = 100
    BITSPERFRAME = 32
    symbols = [x for x in range(start + 200, start + 200 + BITSPERFRAME * 100, 100)]
    end = 100 * BITSPERFRAME + start + 200 + 200
    with open(r"est.png", "rb") as file:
        msg = file.read()
        print(f"msg is of {len(msg)} bytes and will take {len(msg) / 5.5} seconds")
        rx = receiver(25, "TANDBERG", {"start": start, "end": end, "data": list(reversed(symbols))})
        tx = transmitter(180,"2nd output",{"start": start, "end": end, "data": list(reversed(symbols))})
        rx.start_receive()
        for i in range(0, len(msg), 4): 
            x = int.from_bytes(msg[i:i+4])
            tx.transmit_data(x,2)   
        rx.stop_receieve()

    recording.clear()
    record_thread.join()

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Combine into a single int16 numpy array
    audio = np.frombuffer(b"".join(frames), dtype=np.int16)
    #plot_spectrum(np.fft.fft(audio),44100)
    sp = spectrogram(audio, 50,0, 0)
    sp.display_spectrogram()
    sp.show()

def bitstring_to_bytes(s):
    bits = s[2:] if s.startswith('0b') else s
    bits = bits.zfill((len(bits) + 7) // 8 * 8)
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))


if __name__ == "__main__":
    # time.sleep(5)
    start = 100
    msg_path = ""

    BITSPERFRAME = 32
    symbols = [x for x in range(start + 200, start + 200 + BITSPERFRAME * 100, 100)]
    end = BITSPERFRAME + start + 200 + 200
    msg = open(msg_path,"r").read()
    print(f"msg is of {len(msg)} bytes and will take {len(msg) / 5.5} seconds")
    rx = receiver(25, "TANDBERG", {"start": start, "end": end, "data": list(reversed(symbols))})
    tx = transmitter(180,"2nd output",{"start": start, "end": end, "data": list(reversed(symbols))})
    rx.start_receive()
    for i in range(0, len(msg)): 
        x = msg[i]
        tx.transmit_data(x, 1.5)   
    rx.stop_receieve()
    print(rx.get_bstrs())
    with open (r"res.png", "wb") as out:
        for bstr in rx.get_bstrs():
            out.write(bitstring_to_bytes(bstr))
    

    # spectrum_snapshot()



    