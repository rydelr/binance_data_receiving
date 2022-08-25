import websocket
import json
import subprocess
import time
import os, os.path

trade_pair = 'xmrusdt'
socket = f"wss://stream.binance.com:9443/ws/{trade_pair}@trade"
path = f"datastream/{trade_pair}/recent_trades_{trade_pair}.txt"


def on_message(ws, message):
    data = json.loads(message)
    price = data['p']
    quantity = data['q']
    is_buy = data['m']
    timing = data['E']
    trade = f"{str(timing)} {str(price)} {str(quantity)} {str(is_buy)}"
    try:
        with open(path, "a+") as datastream:
            datastream.write(f"{trade} \n")

    except FileNotFoundError:
        print("Datastream file not found, creating new file...")

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as datastream:
            datastream.write(f"{trade} \n")

        print("Datastream file created.")

    else:
        print(trade)


def on_close(ws):
    print("### CONNECTION TERMINATED ###")
    time.sleep(15)
    subprocess.call("datastream.py", shell=True)


ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)

ws.run_forever(ping_interval=100)
