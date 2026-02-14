import pandas as pd
import glob

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

import os
import glob
import pandas as pd

def load_and_concat(folder=".", pattern="*.csv"):
    paths = sorted(glob.glob(os.path.join(folder, pattern)))
    if not paths:
        raise FileNotFoundError(f"No CSVs found in {folder} matching {pattern}")

    dfs = []
    skipped = []

    for p in paths:
        # quick file-size guard
        try:
            if os.path.getsize(p) == 0:
                skipped.append((p, "0 bytes"))
                continue
        except OSError as e:
            skipped.append((p, f"os error: {e}"))
            continue

        try:
            df = parser(p)  # <-- your existing parser() function
            # Guard in case parser returns empty DF
            if df is None or df.empty:
                skipped.append((p, "parsed empty dataframe"))
                continue

            df["__source_file"] = os.path.basename(p)  # optional
            dfs.append(df)

        except pd.errors.EmptyDataError:
            skipped.append((p, "EmptyDataError (likely empty or only skipped rows)"))
        except Exception as e:
            skipped.append((p, f"parse error: {type(e).__name__}: {e}"))

    if not dfs:
        msg = "No valid CSVs to concatenate.\nSkipped:\n" + "\n".join([f"- {p}: {r}" for p, r in skipped])
        raise RuntimeError(msg)

    big = pd.concat(dfs, ignore_index=True)

    # Optional: sort if you have a time column
    if "timestamp" in big.columns:
        big = big.sort_values(["internal_channel_id", "timestamp"]).reset_index(drop=True)

    # Print skipped summary (or return it)
    if skipped:
        print("\nSkipped files:")
        for p, reason in skipped:
            print(f"  - {p}  [{reason}]")

    return big


