import os
import asyncio
import datetime as dt


class AsyncLogger:
    def __init__(self, path, rollover='daily'):
        self.path = path
        self.rollover = rollover
        self.queue = asyncio.Queue()
        # Create an event to signal the completion of the logger
        '''An Event object manages an internal flag that can be set
        to true with the set() method and reset to false with the
        clear() method. The wait() method blocks until the flag is
        set to true. The flag is set to false initially.'''
        self.finished = asyncio.Event()
        self.task = None

    async def _write(self, message):
        current_time = dt.datetime.now() 
        '''There's an option here to choose between 'daily' and '5sec'
        because it's difficult to see how whether the logger does indeed
        generate a new file as we cross midnight. Here, selecting "5sec" does do the job.'''
        if self.rollover == 'daily':
            # Create a new file for each day 
            file_name = f"{current_time.strftime{'%Y%m%d'}}.txt"
        elif self.rollover == '5sec':
            interval = current_time.second // 5
            # Create a new file every 5 seconds 
            file_name = f"{current_time.strftime('%Y%m%d%H%M')}{interval}.txt"
        else:
            raise ValueError(f"Invalid rollover value: {self.rollover}")
        file_path=os.path.join(self.path, file_name)
        print("writing message:", message)
        print(file_path)
        with open(file_path, 'a') as f:
            f.write(current_time.strftime('%Y%m%d%H%M')+": "+ message+"\n") # Write the log message to the file 

    # This is the consumer
    async def _run(self):
        print("running now!")
        while not self.finished.is_set() or not self.queue.empty():
            print(self.queue)
            try: 
                message = await self.queue.get() # Retrieve a message from the queue 
                # Write the message to the log file 
                await self._write(message)
                print("awaiting message write:", message)
            except asyncio.QueueEmpty:
                pass

    def log(self, message):
        try: 
            #Enqueue the log message without waiting 
            print("processing message:", message)
            self.queue.put_nowait(message)

        except asyncio.QueueFull:
            # The queue is not going to be full as maxlength is zero
            pass

    # default to waiting for all logs to be processed 
    async def stop(self, immediately= False):
        self.finished.set()
        if immediately: 
            self.task.cancel()
        else: 
            await self.task
    
    def start(self):
        self.task = asyncio.create_task(self._run()) 


logger = AsyncLogger("./")
async def try_logger():
    

