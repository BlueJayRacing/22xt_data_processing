import pandas as pd
import os 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
# for parsing the data found in the Butler folder 

def parser(file):
    data = pd.read_csv(file, skiprows=1)
    df = data[["recorded_time_ms", "internal_channel_id", "value"]]
    # channel 32 appears signed so unsign it to be consistent with other two channels
    df.loc[df["internal_channel_id"] == 32, "value"] -= 2**32
    # scale down values
    df["value"] /= 65536
    df["recorded_time_ms"] -= 878018
    # get rid of erroneous values 
    df = df.loc[df["value"] < 20000]


    return df

def plot(df):
    # adjust size of dataset 
    df = df.head(20000)
    time = df["recorded_time_ms"]
    value = df["value"]
    # color code by channel - 30: yellow; 31: red; 32: blue
    col = np.where(df["internal_channel_id"] == 30, "y", np.where(df["internal_channel_id"] == 31, "r", "b"))
    # create color map for legend
    colors_map = [
        mlines.Line2D([], [], color="yellow", marker="o", linestyle="none", markersize=8, label="Channel 30"),
        mlines.Line2D([], [], color="red", marker="o", linestyle="none", markersize=8, label="Channel 31"),
        mlines.Line2D([], [], color="blue", marker="o", linestyle="none", markersize=8, label="Channel 32")
    ]
    plt.scatter(time, value, c=col)
    plt.legend(handles=colors_map, title="Channel IDs")
    plt.xlabel("time")
    plt.ylabel("value")
    plt.title("data")
    plt.show()

if __name__ == "__main__":
    file_path = os.path.join("C:", "Users", "Jacki", "OneDrive", "Documents", "Python", "Bajablast", "data_20190101_001815.csv")
    file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\data_20190101_001815.csv"
    df = parser(file_path)
    plot(df)


        
