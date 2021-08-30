import numpy as np
import rrcf
import sys
from pymongo import MongoClient

result_table = MongoClient().rrcf_beta.d3
tw_freq_table = MongoClient().rrcf_beta.tft3

def entry(id,time,point,avg_codisp):
    post = {
        "_id" : id,
        "Time": time,
        "Point": point,
        "Average Codisp": avg_codisp 
    }
    return post
    
def freq_entry(avg_codisp):
    post = {
        "Average Codisp" : avg_codisp        
    }
    return post

filename = sys.argv[1]

lines = open("vectors/vectors_" + filename).read().split('\n')
time = open('time/time_' + filename).read().split('\n')
open('result/result_' + filename,'w')
X = np.array([eval(line) for line in lines])

point_data = open("point_data.csv",'w')
point_data = open("point_data.csv",'a')
count = 0

# Set tree parameters
num_trees = 40
shingle_size = 1
tree_size = 256

# Create a forest of empty trees
forest = []
for _ in range(num_trees):
    tree = rrcf.RCTree()
    forest.append(tree)

# Use the "shingle" generator to create rolling window
# points = rrcf.shingle(X, size=shingle_size)

# Create a dict to store anomaly score of each point
avg_codisp = {}
table = {}
ptr = 0
average_vector = [0,0,0,0]
# For each shingle...
for index, point in enumerate(X):
    # For each tree in the forest...
    #print(point[0], point[1])
    average_vector[0] = (average_vector[0]*(index) + point[0])/(index + 1)
    average_vector[1] = (average_vector[1]*(index) + point[1])/(index + 1)
    average_vector[2] = (average_vector[2]*(index) + point[2])/(index + 1)
    average_vector[3] = (average_vector[3]*(index) + point[3])/(index + 1)

    for tree in forest:
        # If tree is above permitted size...
        if len(tree.leaves) > tree_size:
            # Drop the oldest point (FIFO)
            tree.forget_point(index - tree_size)
        # Insert the new point into the tree
        tree.insert_point(point, index=index)
        # Compute codisp on the new point...
        new_codisp = tree.codisp(index)
        # And take the average over all trees
        if not index in avg_codisp:
            avg_codisp[index] = 0
        avg_codisp[index] += new_codisp / num_trees

    #print(str(index) + ' ' + str(point))
    time_ = time[ptr]
    ptr += 1 
    #points = point.split(',')
    # open('result/result_' + filename,'a').write(str(time_) + ',' + str(point) + ',' + str(avg_codisp[index]) + '\n')
    count += 1
    # total_windows = index
    # result_table.insert_one(entry(count,str(time_),str(point[0]),float(avg_codisp[index])))
    # tw_freq_table.update_one({"Time" : (time_)},{"$set" : freq_entry(float(avg_codisp[index]))})
    #if count > 10:
    #    break
    #print(str(point)[1:-1] + "  " + str(avg_codisp[index]))

#print(avg_codisp)
print(average_vector)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:red'
ax1.set_ylabel('Data', color=color, size=14)
ax1.plot(X, color=color)
ax1.tick_params(axis='y', labelcolor=color, labelsize=12)
ax1.set_ylim(0,160)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('CoDisp', color=color, size=14)
ax2.plot(pd.Series(avg_codisp), color=color)
ax2.tick_params(axis='y', labelcolor=color, labelsize=12)
ax2.grid('off')
ax2.set_ylim(0, 160)
plt.title('X with injected anomaly (red) and anomaly score (blue)', size=14)
plt.show()
