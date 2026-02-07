import pandas as pd

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
    return df

def extract_channel(df, channel):
    return df.loc[df["internal_channel_id"] == channel]

