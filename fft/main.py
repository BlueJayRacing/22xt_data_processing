import utils.parser as parser
import utils.output as output
import utils.butler_parser as butler



if __name__ == "__main__":
    #variables (change these)
    file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\ain.csv"
    cutoff = 20
    fs = 44100
    # allowed_values is an int, work on allowing multiple values in future perhaps 
    allowed_values = 7 

    #functions
    df = butler.parser(file_path, allowed_values)
    x, signal = df["recorded_time_ms"], df["value"]    
    parser.graph(x, signal)
    filtered_signal = parser.high_pass_filter(signal, cutoff, fs)
    windowed_signal = parser.window(filtered_signal)
    Y, N, dt = parser.fft(windowed_signal)
    time = parser.time(dt, Y)
    parser.inverse_fft(time, Y)
    print(Y)

