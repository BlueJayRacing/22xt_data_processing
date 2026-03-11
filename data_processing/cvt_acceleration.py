import matplotlib.pyplot as plt
from fft.utils.parser import load_and_concat, extract_channel


df = load_and_concat(folder = "..//Accessory/", pattern = "data_*.csv")

def plot_channel(df, channel, description = ""):
    channel_data = extract_channel(df, channel)
    time = channel_data["timestamp_us"] / 10**6

    plt.figure(figsize = (12, 4))
    plt.plot(time, channel_data["value"], linewidth = 1, label = f"Channel {channel}")
    plt.xlabel("Time (s)")
    plt.ylabel(f"{description}")
    plt.title(f"Channel {channel} Data")
    plt.legend()
    plt.grid(True, alpha = 0.3)
    plt.tight_layout()
    plt.show()

def main():
    plot_channel(df,16, "Engine RPM")

if __name__ == "__main__":
    main()