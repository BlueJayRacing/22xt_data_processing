import os
import fft.utils.signal_processing as sig
import vis.utils.parser as parser
import vis.utils.grapher as grapher 



def ask_user_channels(allowed_list):
    """Asks user for channels and validates against a master list."""
    while True:
        user_input = input(f"Enter channel IDs from {allowed_list} (separated by spaces): ")
        
        try:
            # 1. Convert input strings to integers
            selected = [int(x) for x in user_input.replace(',', ' ').split()]
            
            # 2. Check if the list is empty
            if not selected:
                print("No numbers detected. Please try again.")
                continue
            
            # 3. Check if all entered numbers are in the 'allowed' list
            # We use a set for a 'subset' check—it's very efficient
            if set(selected).issubset(set(allowed_list)):
                return selected  # Success! This breaks the loop and returns the list
            else:
                # Find exactly which ones were wrong to help the user
                invalid = list(set(selected) - set(allowed_list))
                print(f"Error: {invalid} are not valid options. Only use: {allowed_list}")
                
        except ValueError:
            print("Error: Please enter numbers only (digits and spaces).")

if __name__ == "__main__":

    # DO NOT DELETE
    # This is the only documentation of sampling frequency lol
    #variables (change these)
    cutoff = 150
    fs = 993

    #functions

    #parsing
    df = parser.load_and_concat(folder="Accessory/", pattern="data_*.csv")
    # unique_channels = df["internal_channel_id"].unique()
    # allowed_values = ask_user_channels(unique_channels)
    # grapher.time_plot(df,allowed_values)

    # Max range: 0 to 2920157 (default values)
    # Approx. time of race: 1600000 to 2200000
    grapher.btr_linpot_plot(df, "d", 1600000, 2200000)
    grapher.btr_linpot_plot(df, "v", 1600000, 2200000)
    grapher.btr_linpot_plot(df, "a", 1600000, 2200000)

    



    