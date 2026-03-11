import matplotlib.pyplot as plt
from fft.utils.parser import load_and_concat, extract_channel
import numpy as np


df = load_and_concat(folder = "..//Accessory/", pattern = "data_*.csv")

KNOBS= {17:37,
        19: 3}

def compute_rpm(channel_data, pulses_per_revolution, window_size = 5):
    time = channel_data["timestamp_us"] / 1e6
    times, rpms = [], []

    for i, t in enumerate(time):
        mask = (time >= t - window_size / 2) & (time <= t + window_size / 2)
        pulse_count = mask.sum()
        rotations = pulse_count / pulses_per_revolution
        rpm = (rotations / window_size) * 60
        times.append(t)
        rpms.append(rpm)

    return np.array(times), np.array(rpms)



def plot_channel(df, channel, description = ""):
    channel_data = extract_channel(df, channel)
    knobs = KNOBS[channel]

    time, rpm = compute_rpm(channel_data, knobs, window_s)

    plt.figure(figsize=(12, 4))
    plt.plot(time, rpm, linewidth=1, label=f"Channel {channel}")
    plt.xlabel("Time (s)")
    plt.ylabel(f"RPM")
    plt.title(f"Channel {channel} — {description} RPM")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    plot_channel(df, 17, "Rear Axel RPM")
    plot_channel(df, 19, "Engine RPM")

if __name__ == "__main__":
    main()