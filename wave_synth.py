import wave
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import struct
import simpleaudio as sa

class wave_data():
    def __init__(self):
        self.data = None
        self.numsamples = None; self.sampwidth = None
        self.samprate = None; self.nchans = None
        self.pack_format = None; self.offset = None

    def parse_to_int(self, bytes):
        #parsed_int = int.from_bytes(bytes, byteorder=sys.byteorder, signed=False)
        parsed_int = struct.unpack(self.pack_format,bytes)
        #print('Bytes ' + str(bytes) + "| Integer " + str(parsed_int))
        return parsed_int

    def read_wav(self, filename):
        int_list = []
        with wave.open(filename, 'rb') as wv:
            self.numsamples = wv.getnframes(); self.sampwidth = wv.getsampwidth()
            self.samprate = wv.getframerate(); self.nchans = wv.getnchannels()
            offsets = (None,127, 0, None,0)
            self.offset = offsets[self.sampwidth]
            formats = (None,'B','h',None,'l')
            self.pack_format = formats[self.sampwidth]*self.nchans
            for x in np.arange(numsamples):
                frame = wv.readframes(1)
                int_list.append(self.parse_to_int(frame))
            wv.close()
        self.data = int_list
        return int_list

    def parse_to_bytes(self, signal, nchannels, right_signal=None):
        if isinstance(signal, list):
            pass
        else:
            signal = int(signal)
            #parsed_bytes = signal.to_bytes(num_bytes, byteorder=sys.byteorder, signed=False)
            if (nchannels == 1):
                parsed_bytes = struct.pack(self.pack_format, signal)
            else:
                parsed_bytes = struct.pack(self.pack_format, signal, right_signal)
        return parsed_bytes

    def make_wav(self, nchannels,sampwidth,samprate,numsamples,signal,right_sig=None):
        self.numsamples = numsamples; self.sampwidth = sampwidth
        self.samprate = samprate; self.nchans = nchannels
        offsets = (None,127, 0, None,0)
        self.offset = offsets[self.sampwidth]
        formats = (None,'B','h',None,'l')
        self.pack_format = formats[self.sampwidth]*self.nchans
        with wave.open('output2.wav', 'wb') as newwv:
            newwv.setnchannels(nchannels)
            newwv.setsampwidth(sampwidth)
            newwv.setframerate(samprate)
            #newwv.setnframes(numsamples)
            if(nchannels == 1):
                bytearray_list = [ self.parse_to_bytes((x+self.offset),nchannels) for x in signal ]
            else:
                bytearray_list = [ self.parse_to_bytes((signal[x]+self.offset),nchannels, right_signal = (right_sig[x]+self.offset)) for x in range(len(signal)) ]
            for bytearray in bytearray_list:
                newwv.writeframesraw(bytearray)
            newwv.close()


def generate_sine_tone(numsamples, sampwidth, sample_time, frequency):
    scale = 2**(sampwidth * 8 - 1) - 1
    t = np.arange(numsamples) * sample_time # Time vector
    signal = scale*np.sin(2*np.pi * frequency*t) #+\
    #scale*np.sin(2*np.pi * 300*t)
    return signal

if __name__ == "__main__":
    nchannels = 1
    sampwidth = 2
    duration = 2
    samprate = 44100 # Sampling rate
    numsamples = samprate*duration# Sample count
    st = 1.0 / samprate # Sample time

    signal = generate_sine_tone(numsamples, sampwidth, st, 100)
    signal2 = signal.astype(np.int16)
    if (nchannels == 1):
        right_signal = None
    else:
        right_signal = signal.astype(np.int16)
    #Play generated tone to verify
    play_obj = sa.play_buffer(signal2, nchannels, sampwidth, samprate)

    new_wav_data = wave_data()
    new_wav_data.make_wav(nchannels,sampwidth,samprate,numsamples,signal,right_sig=right_signal)
