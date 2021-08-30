import sys
import os

file_list = []

for file in os.listdir():
    if file[-4:] == ".csv":
        file_list.append(file)

for filename in file_list:
    lines = open(filename,'r').read().split('\n')
    # open(filename,'w')

    # new_lines = []
    for line in lines:
        arr = line.split(',')
        if arr[0] == " Time" or arr[0] == "Time":
            continue
        if len(line) < 5:
            continue
        arr[0] = int(arr[0])
        # new_lines.append(line)
        #print("\'" + str(arr[0]) + "\'")

    def sortSecond(val):
        return val[0]

    #lines.sort(key=sortSecond)
    lines.sort()

    # open(filename,'a').write('Time, Duration, Source IP, Total Bytes, Entropy, Total Domiains')
    start = 0
    for line in lines:
        if len(line) < 3:
            continue
        if start == 0:
            open(filename,'w').write(str(line) + '\n')
            start = 1
        else:
            open(filename,'a').write(str(line) + '\n')
