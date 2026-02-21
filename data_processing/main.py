import os
import fft.utils.signal_processing as sig
import fft.utils.parser as parser
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
    # file_path = os.path.join("C:", "Users", "Jacki", "OneDrive", "Documents", "Python", "Bajablast", "data_20190101_001815.csv")
    # file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\ain.csv"
    file_path = "./data_20251018_131108.csv"
    
    # file_path = "fft/utils/data_20251018_132908.csv"
    #variables (change these)
    cutoff = 150
    fs = 993

    #functions

    #parsing
    df = parser.load_and_concat(folder="Accessory/", pattern="data_*.csv")
    # unique_channels = df["internal_channel_id"].unique()
    # allowed_values = ask_user_channels(unique_channels)
    # grapher.time_plot(df,allowed_values)

    df_small = parser.extract_channel(df, 6)
    x = (df_small["timestamp_us"] - 1760793074020350) / 10**6
    signal = df_small["value"] 
    # signal = signal - 10000000
    grapher.line_plot(x, signal)
    filtered_signal = sig.high_pass_filter(signal, cutoff, fs)
    windowed_signal = sig.window(filtered_signal)
    grapher.spectrogram_plot(windowed_signal)

    # #signal processing 
   
    # freqs, Y, fft_signal, N, dt = sig.fft(windowed_signal)
    # grapher.line_plot(freqs, fft_signal, "FFT Signal", "frequency bins", "amplitude")
    # time = sig.time(dt, Y)
    # inverse_signal = sig.inverse_fft(Y)
    # grapher.line_plot(time, inverse_signal, "Inverse FFT", "time", "amplitude")
    



    