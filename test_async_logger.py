import os
import asyncio
import datetime as dt
import unittest

from async_logger import AsyncLogger


class TestAsyncLogger(unittest.TestCase):
    def setUp(self):
        self.log_dir = "./test_logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.logger = AsyncLogger(self.log_dir)

    def tearDown(self):
        self.logger.stop(immediately=True)
        files = os.listdir(self.log_dir)
        for file in files:
            os.remove(os.path.join(self.log_dir, file))
        os.rmdir(self.log_dir)
        self.loop.close()

    async def run_test_log_message_written(self, log_message):

        self.logger.start()
        self.logger.log(log_message)
        await asyncio.sleep(0.1)
        print("look here!", self.logger.finished)
        await self.logger.stop()
        print("look here again!", self.logger.finished)

    async def test_log_message_written(self):

        log_message = "Test log message"
        self.loop.run_until_complete(
            self.run_test_log_message_written(log_message))
        files = os.listdir(self.log_dir)
        print(files)
        self.assertTrue(len(files) > 0)
        log_file_path = os.path.join(self.log_dir, files[0])
        print("this is the log_file_path:", str(log_file_path))
        with open(log_file_path, 'r') as f:
            contents = f.read()
            self.assertIn(log_message, contents)

    # async def test_new_files_created_on_midnight_cross(self):
    #     # Arrange
    #     current_time = dt.datetime.now()
    #     yesterday_file_name = (
    #         current_time - dt.timedelta(days=1)).strftime("%Y%m%d.txt")
    #     yesterday_file_path = os.path.join(self.log_dir, yesterday_file_name)
    #     with open(yesterday_file_path, 'w') as f:
    #         f.write("Dummy log")

    #     # Act
    #     self.logger.start()
    #     self.logger.log("Log message")
    #     asyncio.run(asyncio.sleep(0.1))
    #     self.logger.stop()

    #     # Assert
    #     files = os.listdir(self.log_dir)
    #     self.assertTrue(len(files) > 1)

    #     today_file_name = current_time.strftime("%Y%m%d.txt")
    #     self.assertIn(today_file_name, files)
    #     self.assertNotIn(yesterday_file_name, files)

    async def test_stop_behavior_works(self):
        # Arrange
        log_message = "Test log message"

        # Act
        self.logger.start()
        self.logger.log(log_message)
        self.logger.log(log_message)
        self.logger.log(log_message)
        self.logger.stop(immediately=False)

        # Assert
        self.assertTrue(self.logger.queue.empty())

    # def test_stop_behavior_omits_outstanding_logs(self):
    #     # Arrange
    #     log_message = "Test log message"

    #     # Act
    #     self.logger.start()
    #     self.logger.log(log_message)
    #     self.logger.log(log_message)
    #     self.logger.log(log_message)
    #     self.logger.stop(immediately=True)

    #     # Assert
    #     self.assertTrue(self.logger.queue.empty())

    # def test_stop_behavior_waits_for_logs(self):
    #     # Arrange
    #     log_message = "Test log message"

    #     # Act
    #     self.logger.start()
    #     self.logger.log(log_message)
    #     self.logger.log(log_message)
    #     self.logger.log(log_message)
    #     self.logger.stop(immediately=False)

    #     # Assert
    #     self.assertTrue(self.logger.queue.empty())

    # def test_invalid_rollover_value(self):
    #     # Arrange
    #     invalid_rollover = "invalid"

    #     # Act & Assert
    #     with self.assertRaises(ValueError):
    #         logger = AsyncLogger(self.log_dir, rollover=invalid_rollover)


if __name__ == "__main__":
    unittest.main()
