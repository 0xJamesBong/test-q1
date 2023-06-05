import datetime
import json
import websocket
import threading
import time
from collections import defaultdict
import pprint
from myAttempt import AsyncLogger
# https://binance-docs.github.io/apidocs/spot/en/#how-to-manage-a-local-order-book-correctly
# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
pp = pprint.PrettyPrinter(indent=4)


socket = 'wss://stream.binance.com:9443/ws'
orderbook = defaultdict(list)

logger = AsyncLogger(path="./myAttemptLogs/", rollover="10sec")
# logger.log("Hello, World!")
# time.sleep(1)
# logger.stop()


def on_open(ws):
    print("WebSocket opened")

    subscribe_message = {
        "method": "SUBSCRIBE",
        "params":
        [
            "btcusdt@depth@100ms"
        ],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    print("Received a message")
    d = json.loads(message)
    bids = d.get('b')[:5]
    asks = d.get('a')[:5]

    orderbook['bids'] = bids
    orderbook['asks'] = asks

    pp.pprint(d)

    logger.log(f"Top 5 bids: {bids}")
    logger.log(f"Top 5 asks: {asks}")
    # print(f"Top 5 bids: {bids}")
    # print(f"Top 5 asks: {asks}")
#     messages look like
# {   'E': 1685872882070,
#     'U': 37122787130,
#     'a': [['27221.08000000', '0.00000000']],
#     'b': [['27212.36000000', '0.00000000'], ['27084.90000000', '0.00000000']],
#     'e': 'depthUpdate',
#     's': 'BTCUSDT',
#     'u': 37122787133}


def on_close(ws):
    time = datetime.datetime.now()
    logger.log(f"WebSocket closed at: {time}")
    logger.stop()
    print("WebSocket closed")


def on_error(ws, error):
    print(f"Error occurred: {error}")


def start_websocket():
    ws = websocket.WebSocketApp(socket,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close,
                                on_error=on_error)

    while True:
        try:
            ws.run_forever()
        except Exception as e:
            print(f"Exception occurred: {e}. Reconnecting...")
            time.sleep(3)  # prevent aggressive reconnection


def websocket_run(ws):
    ws.run_forever()


def get_some_data():
    start_time = datetime.datetime.now()
    ws = websocket.WebSocketApp(
        socket, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)

    # Run websocket on a separate thread
    ws_thread = threading.Thread(target=websocket_run, args=(ws,))
    ws_thread.start()

    while (datetime.datetime.now() - start_time).total_seconds() < 30:
        time.sleep(1)  # Pause execution for 1 second

    ws.close()
    ws_thread.join()  # Wait for the websocket thread to finish


get_some_data()


# start_websocket()
# wst = threading.Thread(target=start_websocket)
# wst.daemon = True
# wst.start()
