import sys
import os


# Arguments passed
# print("\nName of Python script:", sys.argv[0])
# print("\nArguments passed:", end = " ")
# n = len(sys.argv)
# for i in range(1, n):
#     print(sys.argv[i], end = " ")

# Command Line Arguements - To read user input ✅
myArgs = sys.argv[1:]
# print(myArgs)


usage = '''Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics''';

# Usage - To display help message to users ✅
def taskUsage():
    # print(usage)
    # To avoid (.) while printing "usage"
    sys.stdout.buffer.write(usage.encode('utf8'))


def createDS() :
    try:
        # Read the data from the file
        dirPath = './path/to/apps'
        file = open(f'{dirPath}/task.txt', 'r')
        tasks = file.readlines()
        # Store data in a data structure "ds"
        ds = []
        count = 1
        for task in tasks:
            tSplit = task.split(" ")
            pot = ([int(tSplit[0]), count, " ".join(tSplit[1:]).removesuffix('\n')])
            ds.append(pot)
            count += 1
        file.close()
        return ds
    except:
        return 0

def sortByOrderAndPriority(ds) :
    for i in range(len(ds)-1):
        # If priorities of adjacent elements are equal, sort by insertion order
        if ds[i][0] == ds[i+1][0] :
            ds[i][0],ds[i+1][0]=ds[i+1][0],ds[i][0]
    return ds

def sortTask():
    try:
        dirPath = './path/to/apps'
        ds = createDS()
        # First sort by order
        ds.sort(key = lambda x: x[0])
        # then order by both priority and order
        ds = sortByOrderAndPriority(ds)
        # rewrite based on priority
        with open(f'{dirPath}/task.txt', "w+") as f:
            f.truncate()
            for dsI in ds:
                f.write(f'{dsI[0]} {dsI[2]}\n')
    except:
        return 0


# Add task - add the task given by user to the file ✅
def addTask():
    dirPath = './path/to/apps'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    try:
        file = open(f'{dirPath}/task.txt', 'a+')
        file.write(f'{myArgs[1]} {myArgs[2]}\n')
        file.close()
        print(f'Added task: "{myArgs[2]}" with priority {myArgs[1]}');
        sortTask()
    except:
        print("Error: Missing tasks string. Nothing added!");
        return;


# List task ✅
def lsTask():
    try:
        taskData = createDS()
        count = 1
        for task in taskData:
            printData = (f'{count}. {task[2]} [{task[0]}]\n')
            sys.stdout.buffer.write(printData.encode('utf8'))
            count += 1
    except:
        print("There are no pending tasks!")


def rewrite(data):
    dirPath = './path/to/apps'
    with open(f'{dirPath}/task.txt', "w+") as f:
        f.truncate()
        for dsI in data:
            f.write(f'{dsI[0]} {dsI[2]}\n')

# Delete task ✅
def delTask():
    try:
        delIndex = int(myArgs[1])
        data = createDS()
        if delIndex > len(data) or delIndex <= 0:
            printErrorData = (f'Error: task with index #{delIndex} does not exist. Nothing deleted.')
            sys.stdout.buffer.write(printErrorData.encode('utf8'))
            return
        elif delIndex == 1:
            data = data[1:]
        elif delIndex == len(data):
            data = data[0:len(data)-1]
        else:
            data = data[0:delIndex-1] + data[delIndex:]
        # rewrite based on delIndex
        rewrite(data)
        printData = (f'Deleted task #{delIndex}')
        sys.stdout.buffer.write(printData.encode('utf8'))
    except:
        print("Error: Missing NUMBER for deleting tasks.")


def doneTask():
    try:
        doneIndex = int(myArgs[1])
        data = createDS()
        if doneIndex > len(data) or doneIndex <= 0:
            printData = (f'Error: no incomplete item with index #{doneIndex} exists.')
            sys.stdout.buffer.write(printData.encode('utf8'))
        else:
            pending = []
            completed = []
            if doneIndex == 1:
                completed = data[0:1]
                pending = data[1:]
            elif doneIndex == len(data):
                pending = data[0:doneIndex-1]
                completed = data[doneIndex-1:]
            else:
                pending = data[0:doneIndex-1] + data[doneIndex:]
                completed = data[doneIndex-1:doneIndex]
            # rewrite task.txt based on doneIndex
            rewrite(pending)
            # rewrite completed.txt based on doneIndex            
            dirPath = './path/to/apps'
            with open(f'{dirPath}/completed.txt', "a+") as f:
                f.write(f'{completed[0][2]}\n')
            print("Marked item as done.")
    except:
        print('Error: Missing NUMBER for marking tasks as done.')



def reportTask():
    try:
        taskData = createDS()
        printPendingData = (f'Pending : {len(taskData)}\n')
        sys.stdout.buffer.write(printPendingData.encode('utf8'))
        lsTask()
        printNewLine = ('\n')
        sys.stdout.buffer.write(printNewLine.encode('utf8'))
        dirPath = './path/to/apps'
        with open(f'{dirPath}/completed.txt', "r") as f:
            tasks = f.readlines()
            printCompletedData = (f'Completed : {len(tasks)}\n')
            sys.stdout.buffer.write(printCompletedData.encode('utf8'))
            count = 1
            for task in tasks:
                printTaskWithIdx = (f'{count}. {task}')
                sys.stdout.buffer.write(printTaskWithIdx.encode('utf8'))
                count += 1
    except:
        print("Pending : 0")
        print()
        print("Completed : 0")


# CLI User Input is channeled to respective function
try:
    if myArgs[0] == 'add':
        addTask();
    elif myArgs[0] == 'ls':
        lsTask();
    elif myArgs[0] == 'del':
        delTask();
    elif myArgs[0] == 'done':
        doneTask();
    elif myArgs[0] == 'help':
        taskUsage();
    elif myArgs[0] == 'report':
        reportTask();
    else:
        taskUsage();
except:
    taskUsage();

# print(doneTask())
