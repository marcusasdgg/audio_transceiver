# we will make advantage of our analysis class hook by:
# adding all possible symbols in listened frequencies
# we have internal state tracking listening state
# when our start symbol in set we will set track freq to on
# when our end symbol in set we will set track freq to off
# we take an average of the data plots between the 2 events and find the bytes we want

# in terms of resolution we can probably make the window size like 50ms and it will be fine
# we probably want some leeway in tones so our transeiver will output a tone of 100ms length.
# yielding an output of 10 bytes ps

# we can increase symbol count to multiply our data by 2 each time instead of shorteneing recording time.
from enum import Enum
import audio.analysis as an
import pyaudio
import time

from .helpers import find_first_dev

class listen_state(Enum):
    STARTED = 0
    STOPPED = 1

class receiver: 
    # symbols is a dictionary of : {
    # start = (freq)
    # end = (freq)
    # data = [freq,freq,freq]
    #}
    def __init__(self, sample_length_ms, mic_name, symbols):
        p = pyaudio.PyAudio()

        index, dev = find_first_dev(p,mic_name)
        self.sample_rate = int(dev["defaultSampleRate"])
        
        self.state = listen_state.STOPPED
        self.sample_length = sample_length_ms / 1000
        self.mic_name = mic_name
        self.start = symbols["start"]
        self.end = symbols["end"]
        self.data_sy = symbols["data"]
        self.decoded_data = []
        self.once = False

        # initalise our analyzer    
        sy = symbols["data"] + [self.start, self.end]
        self.analyzer = an.freq_analyser(sy, 5, self.sample_rate)

        # initalise our microphone
        stream = p.open(
            format= pyaudio.paInt16,
            channels=1, 
            rate=44100, 
            frames_per_buffer= int(44100 * 0.050),
            input_device_index=index, 
            input=True
        )
        
        # pass our stream to freq analyser.
        self.analyzer.add_hook(stream, self.stream_handler,  int(44100 * 0.050))
        return

    def start_receive(self):
        with open("log.txt","w") as file:
            None
        self.analyzer.start()

    def stop_receieve(self):
        self.analyzer.release_hook()

    def log_set(self, symbol_set, path_name = "log.txt"):
        with open(path_name,"a") as file:
            
            s = ",".join([f"{x}" for x in symbol_set])
            file.write(f"LOG {time.time()} detected set [{s}]\n")

    def add_log(self, contents, path_name = "log.txt"):
         with open(path_name, "a") as file:
            file.write(f"LOG {time.time()}: {contents}\n")

    def get_bstrs(self):
        return self.decoded_data

    def stream_handler(self, symbol_set):
        #self.log_set(symbol_set)
        if self.start in symbol_set:
            if (self.state == listen_state.STARTED):
                #self.add_log("ERROR found start symbol whilst state is start")
                return
            #self.add_log("FOUND START FRAME")
            self.state = listen_state.STARTED
        elif self.end in symbol_set:
            if (self.state == listen_state.STOPPED):
                #self.add_log("ERROR found start symbol whilst state is start")
                return
            #self.add_log("FOUND END FRAME")
            self.state = listen_state.STOPPED
            self.once = False
        else:
            if (self.state == listen_state.STARTED and self.once == False):
                self.once = True
                bstr =  "0b" + "".join(["1" if x in symbol_set else "0" for x in self.data_sy])
                self.decoded_data.append(bstr)
                
        return