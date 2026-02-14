# Python used for visualizing graphs
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy.signal import spectrogram
import numpy as np



def time_plot(df, allowed_values):
    """
    Gemerates time-domain graph(s) for individual channels in the DataFrame

    Args:
        df (pd.DataFrame): pandas DataFrame
        allowed_values (list[int]): A list of channel IDs to retain.

    Returns:
        None
    """ 

    # adjust size of dataset 
    # df = df.head()
    num_channels = len(allowed_values)
    cols = 2
    rows = math.ceil(num_channels / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows), squeeze=False)
    if num_channels == 1:
        axes_flat = [axes]
    else:
        axes_flat = axes.flatten()
    cmap = plt.get_cmap('tab10')
    for i, n in enumerate(allowed_values):
        ax = axes_flat[i]
        to_plot = df.loc[df["internal_channel_id"] == n]
        ax.plot(to_plot["recorded_time_ms"], 
                to_plot["value"], 
                linestyle="solid", 
                linewidth=1, 
                c=cmap(i % 10)) # Loops colors if > 10 channels
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Value")
        ax.set_title(f"Butler Channel {n}")
        ax.grid(True, alpha=0.3)
    for j in range(num_channels, len(axes_flat)):
        axes_flat[j].axis('off')

    plt.tight_layout() # Much cleaner than subplots_adjust(hspace=1)
    plt.show()


def scat_plot(x, y, title="Graph", xlabel="x", ylabel="y"):
    '''
    Creates scatter plot
    
    Args:
        x: list of number values
        y: list of number values

    Returns:
        None
    '''
    plt.scatter(x, y, color="blue")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()


def line_plot(x, y, title="Graph", xlabel="x", ylabel="y"):
    '''
    Creates line plot
    
    Args:
        x: list of number values
        y: list of number values 

    Returns:
        None
    '''
    # add stuff so that we can createsubplots
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def spectrogram_plot(signal):
    f, t_spec, Sxx = spectrogram(
        signal,
        fs=993,
        window='hann',
        nperseg=256,
        noverlap=int(0.75 * 256),
        scaling='density',
        mode='magnitude'
    )

    Sxx_dB = 10 * np.log10(Sxx + 1e-12)

    # Plot
    plt.figure(figsize=(8,4))
    plt.pcolormesh(t_spec, f, Sxx_dB, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.title('Spectrogram')
    plt.colorbar(label='Magnitude')
    plt.tight_layout()
    plt.show()