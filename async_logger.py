import os
import asyncio
import datetime


class AsyncLogger:
    def __init__(self, path, rollover="daily"):
        self.path = path
        self.rollover = rollover
        self.queue = asyncio.Queue()    # Create an asynchronous queue
        # Create an event to signal the completion of the logger
        '''An asyncio event can be used to notify multiple asyncio tasks that some event has happened.
        An Event object manages an internal flag that can be set to true with the set() method
        and reset to false with the clear() method.
        The wait() method blocks until the flag is set to true. The flag is set to false initially.'''
        self.finished = asyncio.Event()
        self.task = None

    async def _run(self):
        print("here!")
        while not self.finished.is_set() or not self.queue.empty():

            print(self.queue)

            try:
                # message = await self.queue.get_nowait()  # Retrieve a message from the queue
                message = await self.queue.get()  # Retrieve a message from the queue

                # Write the message to the log file
                await self._write(message)
                print('awaiting message write:', message)
            except asyncio.QueueEmpty:
                pass

    async def _write(self, message):
        current_time = datetime.datetime.now()
        '''There's an option here to choose between 'daily' and '5sec'
        because it's difficult to see how whether the logger does indeed
        generate a new file as we cross midnight. Here, selecting "5sec" does do the job.'''

        if self.rollover == 'daily':
            # Create a new file for each day
            file_name = f"{current_time.strftime('%Y%m%d')}.txt"
        elif self.rollover == '5sec':
            interval = current_time.second // 5
            # Create a new file every 5 seconds
            file_name = f"{current_time.strftime('%Y%m%d%H%M')}{interval}.txt"
        else:
            raise ValueError(f"Invalid rollover value: {self.rollover}")

        file_path = os.path.join(self.path, file_name)
        print("writing message:", message)
        print(file_path)
        with open(file_path, 'a') as f:
            f.write(message + "\n")   # Write the log message to the file

    def log(self, message):
        try:
            # Enqueue the log message without waiting
            print("processing message:", message)
            self.queue.put_nowait(message)

        except asyncio.QueueFull:
            # Handle the situation when the queue is full (you can log an error, ignore it, etc.)
            pass

    # default to waiting for all logs to be processed
    async def stop(self, immediately=False):
        self.finished.set()
        if immediately:
            self.task.cancel()
        else:
            await self.task

    def start(self):
        self.task = asyncio.create_task(self._run())   # Start the logger task


async def run_logger(dir):
    logger = AsyncLogger("./async_logger_logs/", "5sec")
    logger.start()
    logger.log("There was a countess of Bray")
    logger.log("And you may think it odd when I say")
    logger.log("That in spite of her high station, rank and education")
    logger.log("She always spelt cunt with a 'K'")

    await logger.stop()

# Create and run the logger within a new asyncio event loop


def main():
    dir = "./async_logger_logs/"
    if os.path.exists(dir):
        files = os.listdir(dir)
        for file in files:
            os.remove(os.path.join(dir, file))

    if not os.path.exists(dir):
        os.makedirs(dir)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_logger(dir))
    finally:
        pass  # No need to close the event loop


if __name__ == "__main__":
    main()
