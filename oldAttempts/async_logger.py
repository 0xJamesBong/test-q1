import logging
import threading
import os
from datetime import datetime

class AsyncFileLogger:
    def __init__(self):
        self.lock = threading.Lock()
        self.log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self._update_logfile()
        self.queue = []
        self.stop_flag = False
        self.worker = threading.Thread(target=self._write_logs)
        self.worker.start()

    def _update_logfile(self):
        date_str = datetime.now().strftime("%Y%m%d")
        self.log_file = os.path.join(self.log_dir, f"log_{date_str}.txt")
        self.logger = logging.getLogger('AsyncLogger')
        file_handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(file_handler)

    def _write_logs(self):
        while True:
            if self.stop_flag and not self.queue:
                break
            if not self.queue:
                continue
            log = self.queue.pop(0)
            self.logger.info(log)
            if datetime.now().strftime("%Y%m%d") not in self.log_file:
                self._update_logfile()

    def log(self, message):
        with self.lock:
            self.queue.append(message)

    def stop(self, wait=True):
        if wait:
            while self.queue:
                continue
        self.stop_flag = True


import unittest
import time
import os

class TestAsyncLogger(unittest.TestCase):
    def setUp(self):
        self.logger = AsyncFileLogger()

    def test_log_writes_to_file(self):
        message = "This is a test log message."
        self.logger.log(message)
        time.sleep(1)  # Give time to write
        with open(self.logger.log_file, 'r') as f:
            self.assertTrue(message in f.read())

    def test_new_file_after_midnight(self):
        self.logger.log("Pre-midnight log")
        self.logger._update_logfile()  # Force update for testing
        self.logger.log("Post-midnight log")
        time.sleep(1)  # Give time to write
        files = os.listdir(self.logger.log_dir)
        self.assertGreaterEqual(len(files), 2)

    def test_stop_immediately_omits_logs(self):
        self.logger.log("This log will be omitted.")
        self.logger.stop(wait=False)
        time.sleep(1)  # Give time to write
        with open(self.logger.log_file, 'r') as f:
            self.assertFalse("This log will be omitted." in f.read())

    def test_stop_after_logs_writes_all_logs(self):
        self.logger.log("This log will be written.")
        self.logger.stop(wait=True)
        time.sleep(1)  # Give time to write
        with open(self.logger.log_file, 'r') as f:
            self.assertTrue("This log will be written." in f.read())

if __name__ == '__main__':
    unittest.main()
