import datetime
import json
import asyncio
import websockets
from async_logger import AsyncLogger


async def get_orderbook_data():
    logger = AsyncLogger("./orderbook_experiment_logs/", "5sec")
    logger.start()
    socket = 'wss://stream.binance.com:9443/ws'
    orderbook = {'bids': [], 'asks': []}

    async def on_message(message):
        try:
            print("received message:", message)
            d = json.loads(message)
            bids = d.get('b')[:5]
            asks = d.get('a')[:5]

            orderbook['bids'] = bids
            orderbook['asks'] = asks

            logger.log(f"Top 5 bids: {bids}")
            logger.log(f"Top 5 asks: {asks}")
        except (ValueError, TypeError) as e:
            print("Error processing message:", e)

    async with websockets.connect(socket) as ws:
        print("WebSocket opened")

        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@depth@100ms"],
            "id": 1
        }
        await ws.send(json.dumps(subscribe_message))

        while True:
            message = await ws.recv()
            await on_message(message)


async def main():
    await get_orderbook_data()

if __name__ == "__main__":
    asyncio.run(main())
