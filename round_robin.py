
from process import Process
from time import sleep


class round_robin:
    def __init__(self):
        self.time_slice = 1000 # Milliseconds given to a process to execute
        self.ready_queue = [] # Process queue
        self.finished_processes = [] # Holds all finished processes

    def setTimeSlice(self,time):
        self.time_slice = time

    def addToQueue(self,work_load):
        process_name = "Process " + str(len(self.ready_queue))
        self.ready_queue.append(Process(work_load=work_load,process_name=process_name))
        print(process_name + " added")
        sleep(self.time_slice/1000)

    def execute(self):
        if len(self.ready_queue) > 0: # Check if ready_queue is empty
            while len(self.ready_queue) > 0: # Executes while ready_queue has elements
              for process in self.ready_queue: # Checks if process is compleated before anything is done
                if process.isCompleated(): # Adds process to finished_process and remove it from ready_queue
                    self.finished_processes.append(process)
                    self.ready_queue.remove(process)
                    print(process.getName() + " was compleated")
                    sleep(self.time_slice/1000)
                else: # If Process is not compleated
                    print(process.getName() + " is executing")
                    process.execute(self.time_slice)
                    if process.getWorkLoadRemaing() < 0:
                        sleep((self.time_slice + process.getWorkLoadRemaing())/ 1000) # Checks if work_load is less than time_slice. If yes then sleep time is lowered to represet the porcess letting go the processor after its work is compleated
                    else:
                        sleep(self.time_slice/1000) # "Executes" process by waiting for time_slice amount of time in milliseconds.

        else:
            print("Ready queue is empty")



r = round_robin()
r.addToQueue(2001)
r.addToQueue(6080)
r.addToQueue(2000)
r.addToQueue(5000)
r.addToQueue(100)
r.addToQueue(5048)
r.addToQueue(5000)
r.execute()