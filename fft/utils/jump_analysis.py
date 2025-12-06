import numpy as np
import math
import matplotlib.pyplot as plt
import parser
import output


t = np.linspace(0, 2*np.pi, 1000, endpoint=True)
f = 3.0 # Frequency in Hz
A = 1 # Amplitude in Unit
s = A * np.sin(2*np.pi*f*t) # Signal
noise = np.random.normal(0, 0.2, size=s.shape)
s_noisy = s + noise

plt.title("Sinwave")
plt.plot(s_noisy)
plt.xlabel("x")
plt.ylabel("y")
plt.show()

Y = np.fft.fft(s_noisy)
N = int(len(Y)/2+1)
Y[N-4:N+3]

plt.title("Sinwave")
plt.plot(np.abs(Y[:N]))
plt.xlabel("x")
plt.ylabel("y")
plt.show()


freqs = np.fft.fftfreq(len(s_noisy), 1/f)
cutoff = 0.1  # Hz
fft_filtered = Y.copy()
fft_filtered[np.abs(freqs) > cutoff] = 0
plt.plot(np.abs(fft_filtered)[:N])
plt.show()

filtered_signal = np.fft.ifft(fft_filtered)
plt.plot(filtered_signal)
plt.show()
