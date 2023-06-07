import datetime
import json
import websocket
import threading
import time
from collections import defaultdict
import pprint
import asyncio
from async_logger import AsyncLogger
# https://binance-docs.github.io/apidocs/spot/en/#how-to-manage-a-local-order-book-correctly
# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
pp = pprint.PrettyPrinter(indent=4)


async def get_orderbook_data():
    logger = AsyncLogger("./orderbook_experiment_logs/", "5sec")
    logger.start()
    socket = 'wss://stream.binance.com:9443/ws'
    orderbook = {'bids': [], 'asks': []}

    def on_open(ws):

        print("WebSocket opened")

        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@depth@100ms"],
            "id": 1
        }
        ws.send(json.dumps(subscribe_message))

    def on_message(ws, message):
        # print("Received a message")
        d = json.loads(message)
        bids = d.get('b')[:5]
        asks = d.get('a')[:5]

        orderbook['bids'] = bids
        orderbook['asks'] = asks

        logger.log(f"Top 5 bids: {bids}")
        logger.log(f"Top 5 asks: {asks}")

    def on_close(ws, close_status_code, close_msg):
        current_time = datetime.datetime.now()
        logger.log(f"WebSocket closed at: {current_time}")
        logger.stop()
        print("WebSocket closed")

    def on_error(ws, error):
        print(f"Error occurred: {error}")

    ws = websocket.WebSocketApp(socket,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close,
                                on_error=on_error)

    ws.run_forever()


def limerick(n):
    logger = AsyncLogger("./orderbook_experiment_logs/", "5sec")
    logger.start()

    if n % 2 == 0:
        logger.log("There was a countess of Bray")
        logger.log("And you may think it odd when I say")
        logger.log("That in spite of her high station, rank and education")
        logger.log("She always spelt cunt with a 'K'")


async def main():
    # limerick(2)
    await get_orderbook_data()

    # await get_orderbook_data(logger)


# Use the default event loop
if __name__ == "__main__":

    asyncio.run(main())
