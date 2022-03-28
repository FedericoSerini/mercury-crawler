from flask import Flask
import requests

app = Flask(__name__)

symbol = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "DOGEUSDT", "NEOUSDT", "BNBUSDT", "XRPUSDT", "LINKUSDT", "EOSUSDT",
          "TRXUSDT", "ETCUSDT", "XLMUSDT", "ZECUSDT", "ADAUSDT", "QTUMUSDT", "DASHUSDT", "XMRUSDT", "BTTUSDT"]


@app.route('/crawler/ALL', methods=["POST"])
def craw():

    for sim in symbol:
        print('Download dataset '+sim)
        r = requests.get("https://www.cryptodatadownload.com/cdd/Binance_"+sim+"_d.csv")

        c = 0
        normalized_lines = []

        splitted_lines = r.text.split("\n")

        for line in splitted_lines:
            column = line.split(",")
            if c > 0:
                if c == 1:
                    crypto_name = remove_suffix(sim,"USDT")
                    column[0] = column[0].replace("unix", "timestamp")
                    column[7] = column[7].replace("Volume "+crypto_name, "volume_cry")
                    column[8] = column[8].replace("Volume USDT", "volume_fiat")
                    column[9] = column[9].replace("tradecount", "trade_count")
                    normalized_lines.append(column)
                    c = c+1
                else:
                    if len(column) and column[0] != "":
                        column[2] = column[2].replace("/", "")
                        normalized_lines.append(column)
                    c = c+1
            else:
                c = c+1
        print('Saving dataset '+sim)
        f = open("/mercury/"+sim+"_d.csv", "w")

        for line in normalized_lines:
            f.write(line[0]+";"+line[1]+";"+line[2]+";"+line[3]+";"+line[4]+";"+line[5]+";"+line[6]+";"+line[7]+";"+line[8]+";"+line[9]+"\n")
        f.close()

    return {'status': 'ok', 'data': symbol}

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8888)