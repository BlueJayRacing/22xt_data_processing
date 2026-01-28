import utils.parser as parser
import utils.output as output
import utils.butler_parser as butler



if __name__ == "__main__":
    file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\ain.csv"
    x, y = butler.parser(file_path)["recorded_time_ms"], butler.parser(file_path)["value"]
    cutoff = 20
    fs = 44100

    signal = parser.graph(x,y)
    filtered_signal = parser.high_pass_filter(signal, cutoff, fs=fs)
    Y, N, dt = parser.fft(parser.window(filtered_signal))
    time = parser.time(dt, Y)
    parser.inverse_fft(time, Y)
    print(Y)

