import unittest
from datetime import datetime, timedelta
import os
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from logging.handlers import TimedRotatingFileHandler
import logging

import calc


class AsyncLogger:
    """
    This is an asynchronous logger class. It creates logs that are written into a file
    asynchronously and provides control over the rotation of these logs.
    """

    def __init__(self, filename, when='S', interval=30, backupCount=0):
        """
        Initializes a new instance of the AsyncLogger class.

        :param filename: The name of the file where the logs will be written.
        :param when: Specifies the type of interval. Value 'S' means "Seconds".
        :param interval: The time interval for the rotation. With when='S', it's in seconds.
        :param backupCount: The maximum number of backup files to keep. Set to 0 to keep all files.
        """
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.loop = asyncio.get_event_loop()
        self.handler = TimedRotatingFileHandler(
            filename, when=when, interval=interval, backupCount=backupCount)

        # Setting up the format for the logs
        FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
        formatter = logging.Formatter(FORMAT)

        # Setting the formatter for the handler
        self.handler.setFormatter(formatter)

        self.logger = logging.getLogger(filename)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

    async def log(self, message, extra=None):
        """
        Writes a log message into the file. This operation is non-blocking.

        :param message: The message to be logged.
        """
        self.loop.run_in_executor(
            self.executor, self._log_to_file, message, extra)

    def _log_to_file(self, message, extra=None):
        """
        Logs the message using the logger. This method runs on the executor.

        :param message: The message to be logged.
        """
        if extra is None:
            self.logger.info(message)
        else:
            self.logger.info(message, extra=extra)

    def stop(self, wait=True):
        """
        Stops the logger. If wait is True, it waits for all scheduled tasks to finish.
        If wait is False, it stops immediately.

        :param wait: A boolean indicating whether to wait for tasks to finish before stopping.
        """
        if wait:
            self.executor.shutdown(wait=True)
        else:
            self.executor.shutdown(wait=False)


class TestAsyncLogger(unittest.TestCase):

    def setUp(self):
        self.filename = "test.log"
        self.logger = AsyncLogger(self.filename)

    def tearDown(self):
        self.logger.stop(wait=True)
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.filename + ".1"):  # If it exists
            os.remove(self.filename + ".1")

    def test_log(self):
        asyncio.run(self.logger.log("Test message", {
                    'clientip': '192.168.0.1', 'user': 'test_user'}))
        with open(self.filename, "r") as f:
            self.assertIn("Test message", f.read())

    def test_rotation(self):
        before_midnight = datetime.now().replace(hour=23, minute=59, second=59)
        after_midnight = before_midnight + timedelta(seconds=2)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = before_midnight
            asyncio.run(self.logger.log("Test message", {
                        'clientip': '192.168.0.1', 'user': 'test_user'}))
            mock_datetime.now.return_value = after_midnight
            asyncio.run(self.logger.log("Another test message", {
                        'clientip': '192.168.0.1', 'user': 'test_user'}))
        self.assertTrue(os.path.exists(self.filename + ".1"))

    def test_stop(self):
        self.logger.stop(wait=False)
        self.assertTrue(self.logger.executor._shutdown)


if __name__ == '__main__':
    unittest.main()


# def main():
#     # Create an instance of AsyncLogger
#     logger = AsyncLogger("my_app.log")

#     # Run some async tasks which log some messages
#     tasks = [logger.log(f"Log message {i}") for i in range(10)]
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(*tasks))

#     # Stop the logger immediately without waiting for outstanding logs
#     logger.stop(wait=False)
#     print("Stopped logger without waiting")

#     # Create another logger
#     logger2 = AsyncLogger("my_app.log")

#     # Run some async tasks which log some messages
#     tasks = [logger2.log(f"Log message {i}") for i in range(10)]
#     loop.run_until_complete(asyncio.gather(*tasks))

#     # Stop the logger and wait for outstanding logs
#     logger2.stop(wait=True)
#     print("Stopped logger after waiting for outstanding logs")


# if __name__ == "__main__":
#     main()
