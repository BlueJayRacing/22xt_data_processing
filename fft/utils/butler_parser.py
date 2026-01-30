import pandas as pd
import os 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
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
def parser(file, allowed_values):
    data = pd.read_csv(file, skiprows=1)
    df = data[["recorded_time_ms", "internal_channel_id", "value"]].copy()
    # channel 32 appears signed so unsign it to be consistent with other two channels
    df = df.loc[df["internal_channel_id"].isin(allowed_values)]
    df = df.head(20000)
    return df

def plot(df):
    # adjust size of dataset 
    # df = df.head()
    df_first = df.loc[df["internal_channel_id"] == 6]
    df_second = df.loc[df["internal_channel_id"] == 7]


    time_first = df_first["recorded_time_ms"]
    value_first = df_first["value"]
    time_second = df_second["recorded_time_ms"]
    value_second = df_second["value"]
    
    
    # color code by channel - 6: yellow; 7: red; rest: blue
    # use c = col in scatter
    col = np.where(df["internal_channel_id"] == 6, "y", np.where(df["internal_channel_id"] == 7, "r", "b"))
    # create color map for legend
    colors_map = [
        mlines.Line2D([], [], color="yellow", marker="o", linestyle="none", markersize=8, label="Channel 6"),
        mlines.Line2D([], [], color="red", marker="o", linestyle="none", markersize=8, label="Channel 7"),
        mlines.Line2D([], [], color="blue", marker="o", linestyle="none", markersize=8, label="Other")
    ]
    plt.subplot(2,1,1)
    plt.plot(time_first, value_first, linestyle = "solid", linewidth = '2', c = 'blue')
    plt.xlabel("time")
    plt.ylabel("value")
    plt.title("Butler FL Linpot (Preliminary)")
    

    plt.subplot(2,1,2)
    plt.plot(time_second, value_second, linestyle = "solid", linewidth = '2', c = 'red')
    plt.xlabel("time")
    plt.ylabel("value")
    plt.title("Butler FR Linpot (Preliminary)")
    plt.subplots_adjust(hspace=1)
    plt.show()


if __name__ == "__main__":
    file_path = os.path.join("C:", "Users", "Jacki", "OneDrive", "Documents", "Python", "Bajablast", "data_20190101_001815.csv")
    file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\ain.csv"
    df = parser(file_path)
    plot(df)


        
