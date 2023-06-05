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
