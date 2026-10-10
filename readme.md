This project was a test to try transmit and receive information via a speaker and microphone via
frequency modulation i.e. Binary frequency key shifting.

The packet structure of the protocl is relatively simple, in chronological order there is the start symbol which is a unique frequency,
then a variable amount of possible frequencies, our data symbols, which when present signify a particular bit of the packet being 1 else 0.
Then finally ending with a unique end symbol.

Future plans:
Possibly add some reliable transmission mechanism like TCP which checks if the packet is malformed then resends it as well as encoding
ordering information so packets come in order (much less of a big deal as our speaker should always play it chronologically).