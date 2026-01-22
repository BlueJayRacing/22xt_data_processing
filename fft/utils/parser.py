#generate csv file with random numbers 

import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal

def parse_csv(file):
    with open(file, "r") as f:
        # get x and t values
        data = pd.read_csv(f)
        x = data["x"].values
        y = data["y"].values
    return x, y 

def graph(x, y):
    '''
    Docstring for graph
    
    :param x: pandas series
    :param y: pandas series
    :return: y values
    :rtype: pandas series
    '''
    plt.scatter(x, y, color = "blue")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("test graph")
    plt.grid(True)
    plt.show()
    return y

def time(dt, nums):
    '''
    Docstring for time
    
    :param dt: float - time between intervals
    :param num: array 

    :return time: array of values in seconds
    '''
    
    time = np.arange(len(nums)) * dt # time between intervals
    return time

def window(y):
    # window prior to FFT

    window = np.hanning(len(y))
    nums_windowed = window * y
    return nums_windowed
    




def fft(x, sampling_rate = 44100):
    Y = np.fft.fft(x) # fourier transform
    N = int(len(Y)//2+1) # positive frequency bins index
    plt.plot(np.abs(Y[:N]))
    plt.title("amplitude vs. frequency bin")
    plt.xlabel("Frequency bins")
    plt.ylabel("amplitude")
    plt.show()

    nyquist_frequency = sampling_rate / 2
    freqs = np.linspace(0, nyquist_frequency, N)

    plt.plot(freqs, np.abs(Y[:len(freqs)]))
    plt.title("amplitude vs. frequency")
    plt.xlabel("frequency")
    plt.ylabel("amplitude")
    plt.grid(False)
    plt.show()


    hann = np.hanning(len(Y))
    dt = 1 / sampling_rate # time between intervals
    Y_normalized = np.abs(Y) / len(Y)
    freqs = np.fft.fftfreq(len(Y_normalized), dt)
    cutoff = 10  # Hz
    fft_filtered = Y_normalized.copy()
    fft_filtered[np.abs(freqs) > cutoff] = 0

    return Y, N, dt

def inverse_fft(time, Y):
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

def random_csv(filename, pairs = 100, min_value = 0, max_value = 100):
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(("x", "y"))
        for pair in range(pairs): #might need to change this based on what x-values are
            row = (pair, round(random.uniform(min_value,max_value), 2))
            writer.writerow(row)