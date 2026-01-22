import utils.parser as parser
import utils.output as output
import utils.butler_parser as butler



if __name__ == "__main__":
    file_path = r"C:\Users\Jacki\OneDrive\Documents\Python\Bajablast\data_20190101_001815.csv"
    x, y = butler.parser(file_path)["recorded_time_ms"], butler.parser(file_path)["value"]
    Y, N, dt = parser.fft(parser.window(parser.graph(x, y)))
    time = parser.time(dt, Y)
    parser.inverse_fft(time, Y)
    print(N)

