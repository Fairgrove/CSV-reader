import os
import csv
import matplotlib.pyplot as plt
import datetime as dt
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings

def getDataDirs():
    dataDirs = []

    listOfDirs = os.listdir('.\\data')
    rootDataDir = '.\\data\\'
    
    for i in listOfDirs:
        dataDirs.append(rootDataDir + i)

    return dataDirs

def dataDirsToName(dataDirs):
    ret = []
    for i in dataDirs:
        x = i.split("\\")
        ret.append(x[2])
    return ret

def dataFilesToName(filePath):
    ret = []
    for i in filePath:
        x = i.split("\\")
        ret.append(x[3])

    ret.append('all')

    return ret

def getDataPaths(dataDirs):
    dataDirs = '.\\data\\' + dataDirs
    print(dataDirs)

    files = []
    
    for filename in os.listdir(dataDirs):
        if filename.endswith(".csv"):
            # print(os.path.join(directory, filename))
            files.append(os.path.join(dataDirs, filename))
        else:
            continue

    return files

kb = KeyBindings()

@kb.add("c-space")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)

def getFile():
    #choose Directory
    dir_completer = WordCompleter(
        dataDirsToName(getDataDirs()),
        ignore_case=True,
    )

    chooseDir = prompt(
        "Gimme a directory: \n",
        completer=dir_completer,
        complete_while_typing=True,
        key_bindings=kb,
    )
    
    #choose file
    fileCompleter = WordCompleter(
        dataFilesToName(getDataPaths(chooseDir)),
        ignore_case=True,
    )

    chooseFile = prompt(
        "Gimme a directory: \n",
        completer=fileCompleter,
        complete_while_typing=True,
        key_bindings=kb,
    )
    
    chooseFile = '.\\data\\' + chooseDir + '\\' + chooseFile
    return chooseFile

def getRow(filePath):
    with open(filePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        titles = next(csv_reader)
        
    row_completer = WordCompleter(
        titles,
        ignore_case=True,
    )

    chooseTitle = prompt(
        "What data do you want?: \n",
        completer=row_completer,
        complete_while_typing=True,
        key_bindings=kb,
    )

    for i in range(len(titles)):
        if titles[i] == chooseTitle:
            return i, chooseTitle

def readData(filePath, dataRow):
    print ('Plotting ' + filePath)
    raw = [[]]
    timestamp = []
    data = []

    with open(filePath) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        i = 0
        
        for row in csv_reader:
            if(line_count > 0):
                # print (row)
                raw.insert(i,row) #arr[i] = row
                i += 1
                line_count += 1
            
            if(line_count == 0):
                line_count += 1

    for j in range(line_count-1):
        if raw[j][dataRow[0]] == 'NaN':
            j += 1
        else:
            timestamp.insert(j, int(raw[j][0]))
            data.insert(j, float(raw[j][dataRow[0]])) 

    dates = [dt.datetime.fromtimestamp(ts) for ts in timestamp]

    plt.plot(dates, data)
    plt.ylabel(dataRow[1])
    plt.xlabel('Time')
    plt.show()


#getRow('.\data\GOMX4A ADCS - ADCS ukf\gswebdump_GOMX4A_ADCS_adcs_ukf_q_02_02_2018_0000_to_01_05_2018_0000.csv')
while(1):
    f = getFile()
    readData(f, getRow(f))