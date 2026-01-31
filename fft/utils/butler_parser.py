import pandas as pd
import matplotlib.pyplot as plt
import math
# for parsing the data found in the Butler folder 
# channel mapping; 6: front left linpot; 7: front right linpot; 12: rear left linpot; 13: rear right linpot


"""Parses a CSV file and filters by specific channel IDs.

    Args:
        file (str): The path to the CSV file to be processed.
        allowed_values (list[int]): A list of channel IDs to retain.

    Returns:
        pd.DataFrame: A DataFrame containing the entire CSV.
                      NOTE: for now, only returning first 20000 entries for dev purposes
"""
def parser(file):
    data = pd.read_csv(file, skiprows=1)
    df = data[["recorded_time_ms", "internal_channel_id", "value"]].copy()
    # channel 32 appears signed so unsign it to be consistent with other two channels
    # df = df.loc[df["internal_channel_id"].isin(allowed_values)]
    df = df.head(20000)
    return df

def time_plot(df, allowed_values):
    # adjust size of dataset 
    # df = df.head()
    num_channels = len(allowed_values)
    cols = 2
    rows = math.ceil(num_channels / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
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
    


        
