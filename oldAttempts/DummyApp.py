
import asyncio
from AsyncLogger import AsyncLogger


async def main():
    # Create an instance of AsyncLogger
    logger = AsyncLogger("my_app.log")

    # Run some async tasks which log some messages
    for i in range(10):
        # Logging context details with the log message
        extra = {'clientip': '192.168.0.1', 'user': f'User-{i}'}
        await logger.log(f"Log message {i}", extra)
        await asyncio.sleep(1)  # Sleep for 1 second

    # Stop the logger and wait for outstanding logs
    logger.stop(wait=True)
    print("Stopped logger after waiting for outstanding logs")


if __name__ == "__main__":
    asyncio.run(main())
