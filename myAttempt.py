import os

'''Python's in built Lists are quite slow for this purpose
because inserting or deleting an element at the beginning requires 
shifting all of the other elements by one, requiring O(n) time.

So we are using queue'''
import queue

import threading
import datetime
import time


class AsyncLogger:
    def __init__(self, path, rollover="daily"):
        # 86400 seconds in a day
        self.path = path
        self.rollover = rollover
        self.queue = queue.Queue()
        self.finished = threading.Event()
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while not self.finished.is_set() or not self.queue.empty():
            try:
                message = self.queue.get(timeout=1)
                self._write(message)
            except queue.Empty:
                pass

    def _write(self, message):
        current_time = datetime.datetime.now()  # Get current time

        # Choose the file name based on the rollover parameter
        if self.rollover == 'daily':
            file_name = f"{current_time.strftime('%Y%m%d')}.txt"
        elif self.rollover == '10sec':
            interval = current_time.second // 10  # Integer division to get either 0 or 1
            file_name = f"{current_time.strftime('%Y%m%d%H%M')}{interval}.txt"
        else:
            raise ValueError(f"Invalid rollover value: {self.rollover}")

        file_path = os.path.join(self.path, file_name)
        with open(file_path, 'a') as f:
            f.write(message + "\n")  # Write the log message to the file

    def log(self, message):
        try:
            self.queue.put(message)
        except Exception as e:
            # Logger should not halt the main application,
            # so we silently catch and discard exceptions
            pass

    def stop(self, immediately=True):
        if immediately:
            while not self.queue.empty():
                self.queue.get()
        self.finished.set()
        self.thread.join()


# Usage example
# logger = AsyncLogger("./myAttemptLogs/")
# logger.log("Hello, World!")
# time.sleep(1)
# logger.stop()
