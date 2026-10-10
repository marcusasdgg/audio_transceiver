This project was a test to try transmit and receive information via a speaker and microphone via
frequency modulation i.e. Binary frequency key shifting.

The packet structure of the protocl is relatively simple, in chronological order there is the start symbol which is a unique frequency,
then a variable amount of possible frequencies, our data symbols, which when present signify a particular bit of the packet being 1 else 0.
Then finally ending with a unique end symbol.

Helping libraries:
To create this project I used pyaudio and numpy, pyaudio to read and write audio samples and numpy for both analysis of a particular sample and 
visualizing it by plotting spectrograms and waterfall graphs. Furthermore as part of my research I created a basic  Fourier transform however
it is slow due to using the standard definition of Discrete Fourier Transform, in my library there is an option to pick between both my implementation
and Numpy's fast fourier transform. 

Future plans:
Possibly add some reliable transmission mechanism like TCP which checks if the packet is malformed then resends it as well as encoding
ordering information so packets come in order (much less of a big deal as our speaker should always play it chronologically).

