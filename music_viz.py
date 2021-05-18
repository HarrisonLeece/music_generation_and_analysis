'''
@author Harrison Leece
@objective - Create a cool visualizer and music data handling package
'''
import numpy as np
import matplotlib.pyplot as plt
import pyaudio as pa
import wave, sys, time, struct

class Visualframe():
    def __init__(self, frames_per_second, sample_freq, wv):
        self.frames_per_second = frames_per_second
        self.sample_freq = sample_freq
        self.waveform = wv
        self.fft = self.fast_ft(wv)
        self.powspec = self.pwr_spec(fft)

    '''
    Fourier transform a list
    The length of the list must be a 2^x number, where x is an integer
    '''
    def fast_ft(self, data_list):
        n=1
        limit = 0
        #This while loop is to allow limit to satisfy the condition in the comment above
        while len(data_list) > limit:
            n+=1
            limit = 2^n
        rfft_data = np.fft.rfft(data_list[0:limit])
        print('rfft data: {}'.format(rfft_data))

        return abs(rfft_data)

    '''
    Inverse Fourier transform a list of frequencies
    '''
    def inverse_ft(self, freq_list):
        ifft_data = np.fft.irfft(freq_list)
        print('ifft data: {}'.format(ifft_data))

        fig3, ax3 = plt.subplots()
        ax3.plot(ifft_data)
        ax3.set_xlabel('Sample_number')
        ax3.set_ylabel('Amplitude')

        return ifft_data

    '''
    Power spectrum density
    '''
    def pwr_spec(self,data_list):
        return abs(data_list)**2

    '''
    Filters
    '''
    def high_pass(fft_list, cutoff):
        assert type(cutoff) is int
        #fft_list should start at 0Hz, with every index representing a frequency
        fft_list[cutoff:] = list(zeros((cutoff,), dtype=int))
        return fft_list

    def mid_pass(fft_list, low_cut, high_cut):
        assert type(cutoff) is int
        #fft_list should start at 0Hz, with every index representing a frequency
        fft_list[low_cut:] = list(zeros((cutoff,), dtype=int))
        fft_list[:high_cut] = list(zeros((cutoff,), dtype=int))
        return fft_list

    def low_pass(fft_list, cutoff):
        assert type(cutoff) is int
        fft_list[:cutoff] = list(zeros((cutoff,), dtype=int))
        return fft_list

    def plot_helper(self):
        pass

class Audioclip():
    def __init__(self, fps, sample_freq, wv):
        self.frames_per = fps
        self.sample_freq = sample_freq
        self.waveform = wv
        self.frames = None
        self.frames_rendered = 0

    #This produces the power spectrum density for the whole audio clip, with no
    #regard for a 'single frame'
    def produce_full_fft(self):
        n=1
        limit = 0
        #This while loop is to allow limit to satisfy the condition in the comment above
        while len(self.waveform) > limit:
            n+=1
            limit = 2^n
        rfft_data = np.fft.rfft(self.waveform[0:limit])
        return abs(rfft_data)
    #This produces the power spectrum density for the whole audio clip, with no
    #regard for a 'single frame'
    def produce_full_pspec(self):
        n=1
        limit = 0
        #This while loop is to allow limit to satisfy the condition in the comment above
        while len(self.waveform) > limit:
            n+=1
            limit = 2^n
        rfft_data = np.fft.rfft(self.waveform[0:limit])
        return abs(rfft_data)**2

    def render_single_frame(self):
        k = int(sample_freq/frames_per_second)
        single_render_waveform = self.waveform[self.frames_rendered*k:(self.frames_rendered*k+k)]
        self.frames_rendered+=1
        return Visualframe(frames_per_second, sample_freq, single_render_waveform)

    #Calling this may cause MEGA-LAG
    def render_frame_data_parse(self, frames_per_second, sample_freq):
        k = int(sample_freq/frames_per_second)
        render_data_list = []
        for n in range(int(num_frames/k)):
            single_render_waveform = self.waveform[n*k:n*k+k]
            single_vizframe = Visualframe(frames_per_second, sample_freq, single_render_waveform)
            render_data_list.append(single_vizframe)
        print('All data in this Audioclip rendered as an array of Visualframes, an instance variable named >frames<')
        self.frames = render_data_list


'''
Parse the wave file's music data to two lists of bytes and ints
adjust the integer values to be easier to plot
'''
def parse_to_int(wav_file):
    frame_list = []
    int_list = []
    num_frames = wav_file.getnframes()
    for i in range(num_frames):
        frame = wav_file.readframes(1)
        frame_list.append(frame)
        int_list.append((int.from_bytes(frame, byteorder=sys.byteorder)))
    return int_list, frame_list


if __name__ == "__main__":
    filename = 'output.wav'
    try:
        with wave.open(filename, mode='rb') as wav_file:
            #Wave package method
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            sample_freq = wav_file.getframerate()
            num_frames = wav_file.getnframes()

            song_length = num_frames/sample_freq
            print(f'Song length:  {song_length}  seconds')

            print('Number of Channels: {}'.format(num_channels))
            print('Sample Width: {}'.format(sample_width))
            print('Sample Frequency: {}'.format(sample_freq))
            print('Number of Frames: {}'.format(num_frames))

            #Get all the frames converted to int and stored in lists
            int_list, frame_list = parse_to_int(wav_file)

            plt.plot(int_list)
            plt.title('music_viz.py input from output.wav')
            #make a Audioclip object, with no major calculations made
            song_audio = Audioclip(60, sample_freq, int_list)
            song_pspec = song_audio.produce_full_pspec()
            song_fft = song_audio.produce_full_fft()
            plt.plot(song_audio.waveform)
            plt.show()

    except Exception as e:
        print(e)
