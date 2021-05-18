import wave
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import struct
import simpleaudio as sa

def parse_to_int(bytes):
    parsed_int = int.from_bytes(bytes, byteorder=sys.byteorder, signed=False)
    #parsed_int = struct.unpack('>h',bytes)[0]
    print('Bytes ' + str(bytes) + "| Integer " + str(parsed_int))
    return parsed_int

def parse_to_bytes(signal):
    if isinstance(signal, list):
        pass
    else:
        num_bytes = 2 #make this an argument later
        signal = int(signal)
        parsed_bytes = signal.to_bytes(num_bytes, byteorder=sys.byteorder, signed=False)
        #parsed_bytes = struct.pack('>h', signal)
    return parsed_bytes

def make_wav(nchannels,sampwidth,samprate,numsamples,signal):
    with wave.open('output2.wav', 'wb') as newwv:
        newwv.setnchannels(nchannels)
        newwv.setsampwidth(sampwidth)
        newwv.setframerate(samprate)
        #newwv.setnframes(numsamples)
        correction = 2**((sampwidth * 8) - 1)
        bytearray_list = [ parse_to_bytes((x+correction)) for x in signal ]
        for bytearray in bytearray_list:
            newwv.writeframes(bytearray)
        newwv.close()
def read_wav(filename):
    int_list = []
    with wave.open(filename, 'rb') as wv:
        numsamples = wv.getnframes()
        for x in np.arange(numsamples):
            frame = wv.readframes(1)
            int_list.append(parse_to_int(frame))
        wv.close()
    return int_list

if __name__ == "__main__":
    duration = 2
    samprate = 44100 # Sampling rate
    numsamples = samprate*duration# Sample count
    st = 1.0 / samprate # Sample time

    nchannels = 1
    sampwidth = 2

    wav_integers = read_wav('output2.wav')
    plt.plot(wav_integers)
    plt.show()
