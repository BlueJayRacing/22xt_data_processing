import matplotlib.pyplot as plt
from fft.utils.parser import load_and_concat, extract_channel
import numpy as np


df = load_and_concat(folder = "..//Accessory/", pattern = "data_*.csv")

KNOBS= {17:37,
        19: 2}

def compute_rpm(channel_data, pulses_per_revolution, window_size = 1):
    time = (channel_data["timestamp_us"].values - channel_data["timestamp_us"].values[0]) / 1e6
    left  = np.searchsorted(time, time - window_size / 2)
    right = np.searchsorted(time, time + window_size / 2)

    pulse_count = right - left
    rpm = (pulse_count / pulses_per_revolution / window_size) * 60
    return time, rpm

def plot_channel(df, channel, description = ""):
    channel_data = extract_channel(df, channel)
    pulses_per_revolution = KNOBS[channel]

    time, rpm = compute_rpm(channel_data, pulses_per_revolution, window_size=1)

    plt.figure(figsize=(12, 4))
    plt.plot(time, rpm, linewidth=1, label=f"Channel {channel}")
    plt.xlabel("Time (s)")
    plt.ylabel(f"RPM")
    plt.title(f"Channel {channel} — {description} RPM")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_engine_vs_axle(df, t_start=None, t_end=None, window_s = 1):
    engine_data = extract_channel(df, 19)
    axle_data   = extract_channel(df, 17)

    t0 = min(engine_data["timestamp_us"].values[0], axle_data["timestamp_us"].values[0])
    engine_data = engine_data.copy()
    axle_data   = axle_data.copy()
    engine_data["timestamp_us"] -= t0
    axle_data["timestamp_us"]   -= t0

    if t_start is not None:
        engine_data = engine_data[engine_data["timestamp_us"] >= t_start * 1e6]
        axle_data   = axle_data[axle_data["timestamp_us"]     >= t_start * 1e6]
    if t_end is not None:
        engine_data = engine_data[engine_data["timestamp_us"] <= t_end * 1e6]
        axle_data   = axle_data[axle_data["timestamp_us"]     <= t_end * 1e6]

    engine_time_s = (engine_data["timestamp_us"].values - engine_data["timestamp_us"].values[0]) / 1e6
    axle_time_s   = (axle_data["timestamp_us"].values   - axle_data["timestamp_us"].values[0])   / 1e6

    left  = np.searchsorted(engine_time_s, engine_time_s - window_s / 2)
    right = np.searchsorted(engine_time_s, engine_time_s + window_s / 2)
    engine_rpm = (right - left) / KNOBS[19] / window_s * 60

    left  = np.searchsorted(axle_time_s, axle_time_s - window_s / 2)
    right = np.searchsorted(axle_time_s, axle_time_s + window_s / 2)
    axle_rpm = (right - left) / KNOBS[17] / window_s * 60
    axle_rpm_interp = np.interp(engine_time_s, axle_time_s, axle_rpm)

    plt.figure(figsize=(8, 6))
    plt.scatter(axle_rpm_interp, engine_rpm, s=20, alpha=0.3)
    plt.xlabel("Rear Axle RPM (Speed)")
    plt.ylabel("Engine RPM")
    plt.title("Engine RPM vs Rear Axle RPM")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def pulse_rate(df, channel):
    data = extract_channel(df, channel)
    time_s = (data["timestamp_us"].values - data["timestamp_us"].values[0]) / 1e6
    total_pulses = len(time_s)
    total_time   = time_s[-1] - time_s[0]
    print(f"Channel {channel}: {total_pulses / total_time:.1f} pulses/sec")

def main():
    plot_channel(df, 17, "Rear Axel")
    plot_channel(df, 19, "Engine")
    plot_engine_vs_axle(df, t_start = 1680, t_end = 1690)
    pulse_rate(df, 17)
    pulse_rate(df, 19)

if __name__ == "__main__":
    main()