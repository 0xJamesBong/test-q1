# Async Logger

This is a simple asynchronous logger implementation in Python. It provides a way to log messages to separate files based on different rollover options.

## Logging Rollover Options

The Async Logger provides two rollover options: "daily" and "5sec". This allows you to control how log files are generated when crossing midnight.

- **Daily Rollover:** With the "daily" option, a new log file is created for each day. The log files are named based on the date in the format `YYYYMMDD.txt`. This option is useful when you want to separate logs by day.

- **5-Second Rollover:** The "5sec" option generates a new log file every 5 seconds. This provides more granularity in log file generation, allowing you to track events with higher precision. The log files are named using the format `YYYYMMDDHHMM{interval}.txt`, where `interval` represents the 5-second interval within the minute. This option is particularly helpful when you need frequent log file updates.

To set the rollover option, initialize the `AsyncLogger` with the desired value, like this:

```python
logger = AsyncLogger("./async_logger_logs/", rollover="5sec")
```

The point of this is to allow one to visually see that the generation of new files - to satisfy the midnight-crossover requirement.

## Files in the Repo

There are 3 files of interest in this repo: `async_logger.py`, `orderbook.py`, and `test_async_logger.py`.

`async_logger.py` is the file where the logger `AsyncLogger` lives. There is a sample implementation of the logger at the end of the file, which is called by `main()`.

run `python3 async_logger.py` and in a directory "./async_logger_logs/" would be generated where a lewd limerick is logged.

```There was a countess of Bray
And you may think it odd when I say
That in spite of her high station, rank and education
She always spelt cunt with a 'K'
```

`orderbook.py` sort of puts the logger into battlefield testing mode. It calls the binance API and the logger is used to log incoming bid and ask orders.

run `python3 orderbook.py` and a directory called "orderbook_logs" would be generated and incoming data would be logged. Since the bid and ask data would be streaming in continuously, the logger, with rollover set to 5sec, would generate a new log file every 5 secs.

`test_async_logger.py` is the testing file. Run:
` python3 -m unittests test_async_logger.py` to run all the tests

# Backend Test Question

## Task

Your task is to create a logging component that writes strings to a text file asynchronously. Below are the detailed requirements.

### Requirements

1. A call to write should be as fast as possible so that the calling application can continue with its work without waiting for the log to be written to the file.
2. If we cross midnight, a new file with a new timestamp must be created. Logs will then be written to the new file.
3. The component must be possible to stop in two ways:
   1. Stop immediately. Any outstanding logs in the pipeline will be omitted.
   2. Wait for the component to finish writing any outstanding logs.
4. If an error occurs during logger operations, the calling application should not halt as a result. It is more important for the application to continue running, even if lines are not being written to the log.
5. Extra points will be awarded for implementing unit tests that ensure:
   1. A call to log will result in something being written.
   2. New files are created when midnight is crossed.
   3. The stop behaviour works as described above.
