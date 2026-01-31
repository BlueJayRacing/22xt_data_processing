import utils.parser as parser
import utils.output as output
import utils.butler_parser as butler

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
    file_path = "fft/utils/data_20251018_132908.csv"
    # df = butler.parser(file_path)
    # unique_channels = df["internal_channel_id"].unique()
    # ask_user_channels(unique_channels)
    # user_input = input("Enter channel(s) you want to plot: ")
    # allowed_values = [int(x) for x in user_input.split()]
    # butler.time_plot(df,allowed_values)

    # #variables (change these)
    # file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\ain.csv"
    cutoff = 20
    fs = 44100
    # allowed_values is an int, work on allowing multiple values in future perhaps 
    allowed_values = [7] 

    #functions
    df = butler.parser(file_path)
    x, signal = df["recorded_time_ms"], df["value"]  
    parser.graph(x, signal)
    filtered_signal = parser.high_pass_filter(signal, cutoff, fs)
    windowed_signal = parser.window(filtered_signal)
    Y, N, dt = parser.fft(windowed_signal)
    time = parser.time(dt, Y)
    parser.inverse_fft(time, Y)
    print(Y)

