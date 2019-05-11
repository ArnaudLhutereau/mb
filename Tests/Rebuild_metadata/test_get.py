import os
import requests

from random import randrange
from threading import Thread



# Parameters
file_name = "test_"
file_number = 100
thread_number = 4
# Class whichs define the thread role
class ExecuteAScript(Thread):

    def __init__(self, min, max, file_name):
        Thread.__init__(self)
        self.min = min
        self.max = max
        self.name = file_name

    def run(self):
        while (self.min < self.max):
        	link = "http://127.0.0.1:3000/"+self.name+str(self.min)+".txt/__meta"
        	requests.get(link)
        	print(link)
        	self.min=self.min+1


# Start 
print("Started")
i = 0
min = 0
max = int(file_number/thread_number)
while(i<thread_number):
    thread_script = ExecuteAScript(min, max, file_name)
    thread_script.start()
    i=i+1
    min = min + int(file_number/thread_number)
    max = max + int(file_number/thread_number)
print("Finished")
