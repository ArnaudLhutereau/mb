import os

from random import randrange
from threading import Thread

###################################
'''
Warning:

1. This test doesn't support bad entries, please be careful
when you choose a number file, a delay between two requests, and a name.

2. When a test is executed, you can't directly generate a new test.
You have to launch again the test tools script because the return of script file generated before
breaks the display.
'''
###################################



# GLOBAL VARIABLES
global file_number # A number
global quit # A string "yes" or "no"
global name_file # A string
global time_sending # A number or or a string "random"
global number_threader
quit = "no"
file_number = None
name_file = None
time_sending = None
number_thread = 8


# Redirect to the appropriate function
def firstChoiceMenu(choice):
    choice = int(choice)
    if(choice == 0):
        configureMenu()
    elif(choice == 1):
        generateScript()
    elif(choice == 2):
        executeTest()
    elif(choice == 3):
        parallelizedScript()
    else:
        global quit
        quit = "yes"

# Display the configuration menu
def configureMenu():
    print("-------------------------\nCONFIGURE MENU")
    print("What do you want to do?")
    print("0 = Choose the file number")
    print("1 = Choose the sending time between two files")
    print("2 = Choose the name of file")
    print("3 = Back to the general menu")
    choice = input()
    choice = int(choice)
    if(choice == 0):
        chooseFileNumber()
    elif(choice == 1):
        chooseTime()
    elif(choice == 2):
        chooseName()

# Choose the file number to send
def chooseFileNumber():
    print("-------------------------\nCHOOSE FILE NUMBER")
    print("Please enter a number, after that you will be automatically teleport in the configure menu.")
    choice = input()
    choice = int(choice)
    global file_number
    file_number = choice
    configureMenu()

# Choose the delay between two requests. Three modes available:
# 0 : as fast as possible
# "random" : random time (between 1 and 4 seconds)
# number : fixed time by number selected by user
def chooseTime():
    print("-------------------------\nCHOOSE TIME SENDING")
    print("Please enter a number which represents the time in seconds between sending two files.")
    print("If you write '0', it means that files are sent as fast as possible.")
    print("If you write 'random', it means that files are sent with a random time delay, between 1 and 3 seconds")
    print("After that you will be automatically teleport in the configure menu")
    choice = input()
    global time_sending
    time_sending = choice
    configureMenu()

# Choose a file name
# Recast doesn't accept two files with the same name
def chooseName():
    print("-------------------------\nCHOOSE FILE NAME")
    print("Please enter a name for file, without the extension.")
    print("First name file will be the name that you give here")
    print("For others files, the name will be the same with a -X where X representes the number")
    print("After that you will be automatically teleport in the configure menu")
    choice = input()
    global name_file
    name_file = choice
    configureMenu()

#  Function which Generates the script and show the total sleep, in case
#  user selected random or fixed time
def generateScript():

    global file_number
    global time_sending
    global name_file
    if(name_file == None or file_number == None or time_sending == None):
        print("\n-------------------------\nERROR")
        print("One of configuration parameters (name of file, number of file or time sending betwen two files aren't filled")
        print("You are automatically teleport in the configure menu\n")
        configureMenu()

    # First, generates all files
    create_files()
    total_sleep = create_script_file()
    os.system('chmod u+x script.sh')
    print("\n-------------------------\nGENERATION OF THE TEST SCRIPT")
    print("You can find in the same directory 'script.sh' which have already execution permissions")
    print("You are automatically teleport in the configure menu")
    print("Total sleep: ", total_sleep,"seconds")

# Execute the file script generates before
def executeTest():

    print("\n-------------------------\nEXECUTION OF THE TEST SCRIPT")
    print("Your script is running")
    print("You are automatically teleport in the configure menu at the end")
    # Start the script test
    os.system('./script.sh')
    configureMenu()

# Create in the same directory "file_number" files
def create_files():
    # Create file_number files in the same directory
    global name_file
    global file_number
    i=0
    while(i<file_number):
        extension = '.'.join([str(i),"txt"])
        fichier = open('_'.join([name_file,extension]),"w")
        fichier.write("test...")
        fichier.close()
        i=i+1

# Creation of the script file, which writes all requests
def create_script_file():
    # Create the script command
    fichier = open("script.sh","w")
    # 3 possibilities
    global file_number
    global time_sending
    global name_file
    total_sleep = 0
    i=0 # Counter
    if(time_sending == "0"):
        # As fast as possible
        while(i<file_number):
            extension = '.'.join([str(i),"txt &\n"])
            file = '_'.join([name_file,extension])
            command = ' '.join(["curl --request PUT http://127.0.0.1:3000/ -T ",file])
            fichier.write(command)
            i=i+1
    elif(time_sending == "random"):
        
        while(i<file_number):
            extension = '.'.join([str(i),"txt\n"])
            file = '_'.join([name_file,extension])
            command = ' '.join(["curl --request PUT http://127.0.0.1:3000/ -T ",file])
            fichier.write(command)
            random_number = randrange(1,4)
            total_sleep = total_sleep + random_number
            time_sleep = ''.join([str(random_number),"\n"])
            command = ' '.join(["sleep", time_sleep])
            fichier.write(command)
            i=i+1

    else:
        while(i<file_number):
            
            extension = '.'.join([str(i),"txt\n"])
            file = '_'.join([name_file,extension])
            command = ' '.join(["curl --request PUT http://127.0.0.1:3000/ -T ",file])
            fichier.write(command)
            total_sleep = total_sleep + int(time_sending)
            time_sleep = ''.join([str(time_sending),"\n"])
            command = ' '.join(["sleep", time_sleep])
            fichier.write(command)
            i=i+1

    fichier.close()
    return total_sleep

# Function which generates and executes the parallelized script
def parallelizedScript():
    
    print("\n-------------------------\nGENERATION  AND EXECUTION OF THE PARALLELIZED TEST SCRIPT")
    print("You can find in the same directory 'scriptX.sh' which have already execution permissions")
    print("You are automatically teleport in the configure menu at the end")
    # Generate script
    parallelizedGeneration()
    # Start script with threads
    parallelizedExecute()

    # Teleport
    configureMenu()

# Function which creates "number_thread" and run all files script
def parallelizedExecute():

    global number_thread
    i=0
    while(i<number_thread):
        thread_script = ExecuteAScript(i)
        thread_script.start()
        i=i+1


# Function which generates "number_thread" files script
def parallelizedGeneration():
    # Global variable
    global file_number
    global time_sending
    global name_file
    global number_thread
    # Create files
    create_files()
    # Threads parameters
    counter_thread=0
    # Local variables
    i = 0
    # Loop for thread
    while(counter_thread<number_thread):
        current_limit=int(file_number/number_thread)*(counter_thread+1)
        if(current_limit == 96):
            current_limit = 100
        # Create the script command for this thread
        file_name_thread = ''.join(["script", str(counter_thread)])
        file_name_thread_extension = '.'.join([file_name_thread,"sh"])
        fichier = open(file_name_thread_extension,"w")

        # Fill the script file
        if(time_sending == "0"):
            # As fast as possible
            while(i<current_limit):
                extension = '.'.join([str(i),"txt &\n"])
                file = '_'.join([name_file,extension])
                command = ' '.join(["curl --request PUT http://127.0.0.1:3000/ -T ",file])
                fichier.write(command)
                i=i+1
        elif(time_sending == "random"):
            # Random time
            while(i<current_limit):
                extension = '.'.join([str(i),"txt\n"])
                file = '_'.join([name_file,extension])
                command = ' '.join(["curl --request PUT http://127.0.0.1:3000/ -T ",file])
                fichier.write(command)
                random_number = randrange(1,4)
                time_sleep = ''.join([str(random_number),"\n"])
                command = ' '.join(["sleep", time_sleep])
                fichier.write(command)
                i=i+1
        else:
            while(i<current_limit):
                # Fixed time
                extension = '.'.join([str(i),"txt\n"])
                file = '_'.join([name_file,extension])
                command = ' '.join(["curl --request PUT http://127.0.0.1:3000/ -T ",file])
                fichier.write(command)
                time_sleep = ''.join([str(time_sending),"\n"])
                command = ' '.join(["sleep", time_sleep])
                fichier.write(command)
                i=i+1

        fichier.close()
        os.system('chmod u+x script{0}.sh'.format(str(counter_thread)))
        counter_thread=counter_thread+1

# Class whichs define the thread role
class ExecuteAScript(Thread):

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id

    def run(self):
        # Find script file
        name_file = ''.join(["./script", str(self.id)])
        name_file_extension = '.'.join([name_file, "sh"])
        os.system('./script{0}.sh'.format(str(self.id)))



# Main script
while(quit != "yes"):
    print("\n-------------------------\nGENERATOR RECAST BLOCKCHAIN TEST")
    print("Welcome in the test time tools for RecastBlockchain")
    print("Here you can configure the tools to modify the number of files, time between sending files...")
    print("What do you want to do?")
    print("0 = Configure")
    print("1 = Generate the test script")
    print("2 = Execute the script")
    print("3 = Generate the parallelized test script and start it")
    
    print("Other to exit")
    choice = input()
    firstChoiceMenu(choice)
