import utils.parser as parser
import utils.output as output



if __name__ == "__main__":
    x, y = parser.parse_csv("../data_19700101_000403.csv")
    Y = parser.fft(parser.window(parser.graph(x, y)))
    time = parser.time(1/2000, Y)
    parser.inverse_fft(time, Y)

