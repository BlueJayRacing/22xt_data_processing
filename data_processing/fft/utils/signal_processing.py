#generate csv file with random numbers 

import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal



def high_pass_filter(sig, cutoff, fs, order=4):
    '''
    Uses high-pass filter to cut out low freqs
    
    :sig: series of signal
    :cutoff: int of cutoff frequency
    :fs: int of sampling frequency

    :return: series of signal
    '''
    nyquist = fs / 2
    normalized_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normalized_cutoff, btype="high", analog=False)
    filtered_signal = signal.filtfilt(b, a, sig)
    return filtered_signal 


def window(y):
    '''
    Windows signal
    
    :y: array of values of signal 
    :return: array values of signal
    '''
    # window prior to FFT
    window = np.hanning(len(y))
    y_win = window * y

    # code below is used for normalization
    # y_filtered = y_win -np.mean(y_win)
    # y_filtered /= np.sum(window) / len(window)

    return y_win

def fft(x, sampling_rate = 44100):
    '''
    Performs fft on sample 
    
    :x: array of values of signal
    :sampling_rate: int of sampling rate 

    Return:
    :Y: array of values of signal
    :N: int of length of signal
    :dt: int of time between samples 
    
    series of signal
    '''
    N = len(x) 
    Y = np.fft.rfft(x) / N # fourier transform
    freqs = np.fft.rfftfreq(N, d=1/sampling_rate)
    

    plt.plot(freqs, np.abs(Y))
    plt.title("amplitude vs. frequency bin")
    plt.xlabel("Frequency bins")
    plt.ylabel("amplitude")
    plt.show()

    

    # plt.plot(freqs, np.abs(Y[:len(freqs)]))
    # plt.title("amplitude vs. frequency")
    # plt.xlabel("frequency")
    # plt.ylabel("amplitude")
    # plt.grid(False)
    # plt.show()

    
    dt = 1 / sampling_rate # time between intervals
    
    # nyquist_frequency = sampling_rate / 2
    # hann = np.hanning(len(Y))
    # Y_normalized = np.abs(Y) / len(Y)
    # freqs = np.fft.fftfreq(len(Y_normalized), dt)
    # cutoff = 10  # Hz
    # fft_filtered = Y_normalized.copy()
    # fft_filtered[np.abs(freqs) > cutoff] = 0

    return Y, N, dt

def time(dt, nums):
    '''
    Docstring for time
    
    :dt: float of time between intervals
    :num: array of values

    :return time: array of intervals
    '''
    
    time = np.arange(len(nums)) * dt # time between intervals
    return time

def inverse_fft(time, Y):
    '''
    Inverse fft
    
    :time: array of time values
    :Y: array of values from fft

    :return: none
    '''

    inverse = np.fft.ifft(Y)
    real = np.real(inverse) # retrieve real numbers only

    plt.plot(time, real)
    plt.title("Inverse FFT")
    plt.xlabel("time")
    plt.xlim(left=0)
    plt.ylabel("amplitude")
    plt.show()










def short_time_fft(window, step_size, sampling_frequency):
    short = signal.ShortTimeFFT(window, step_size, sampling_frequency)
    plt.plot(short)
    plt.xlabel("")
    plt.ylabel("")
    plt.show()

def dc_offset(signal):
    filtered_signal = signal - np.mean(signal)
    return filtered_signal, np.mean(signal)

def parse_csv(file):
    with open(file, "r") as f:
        # get x and t values
        data = pd.read_csv(f)
        x = data["x"].values
        y = data["y"].values
    return x, y 




def random_csv(filename, pairs = 100, min_value = 0, max_value = 100):
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(("x", "y"))
        for pair in range(pairs): #might need to change this based on what x-values are
            row = (pair, round(random.uniform(min_value,max_value), 2))
            writer.writerow(row)