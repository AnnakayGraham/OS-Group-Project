

class Process:
    def __init__(self,work_load,process_name):
        self.work_load = work_load
        self.process_name = process_name

    def isCompleated(self):
        return self.work_load <= 0

    def execute(self,time_slice): # Subtracts time_slice from work_load. The difference is the work left to be done 
        self.work_load -= time_slice

    def getName(self):
        return self.process_name

    def getWorkLoadRemaing(self): # Returns work remaining for process
        return self.work_load