from datetime import datetime as dt
start_time = dt.now()
import math
import numpy as np
import rrcf
from pymongo import MongoClient

open('result_avg_vectors.csv','w')

create_database = 0
dbname = "rrcf_beta_8"

def entry(id,time,point,avg_codisp):
    post = {
        "_id" : id,
        "Time": time,
        "Point": point,
        "Average Codisp": avg_codisp 
    }
    return post

def update_freq_entry(avg_codisp):
    post = {
        "Average Codisp" : avg_codisp        
    }
    return post


def freq_entry(id_,time,vector,dict_,total_bytes):
    temp_dict = {}
    for key, value in dict_.items():
        temp_dict[key.replace('.','_')] = value
    post = {
        "_id" : id_,
        "Time": time,
        "Vector" : vector,
        "Dict":temp_dict,  
        "Total bytes" : total_bytes      
    }
    return post


def avg_vector_entry(id_,filename,vector):
    post = {
        "_id" : id_,
        "IP" : filename,
        "Average Vector" : vector      
    }
    return post




def analysis(filename):
    if create_database == 1:
        tw_freq_table = MongoClient()[dbname][('tft_' + str(filename).split('.')[2] + '_'  + str(filename).split('.')[3])] #timeWindow_freq_table

    id_ = 0
    

    lines = open('dpi_filtered_data/' + filename,'r').read().split('\n')
    #  Time, Duration, Source IP, Total Bytes, Entropy, Total Domains, Dictionary
    #   0  ,   1     ,  2       ,  3         , 4      ,    5         ,     6
    try: 
        prev_start_time =  int(lines[0].split(',')[0])/1000.0   # millisseconds to seconds
    except:
        prev_start_time =  int(float(lines[0].split(',')[0]))/1000.0   # millisseconds to seconds 

    time_window = 5

    ux_time_win = time_window*60*1000/1000.0    # millisseconds to seconds
    total_bytes = 0
    entropy = 0
    total_domains = 0
    total_sessions = 0
    time_window_domain_dict = {}

    # start = 0
    vector = []
    open('vectors/vectors_' + filename,'w')
    open('time/time_' + filename,'w')

    for line in lines:
        if len(line) < 2 or line.split(',')[0] == ' Time':
            continue
        # else:dbname
        #     if start == 0:
        #         prev_start_time =  int(lines[1].split(',')[0])/1000.0   # millisseconds to seconds
        #         time_window = 5

        #         ux_time_win = time_window*60*1000/1000.0    # millisseconds to seconds
        #         total_bytes = 0
        #         entropy = 0
        #         total_domains = 0
        #         total_sessions = 0
        #         time_window_domain_dict = {} 
        #         start = 1


        data_arr = []
        data_arr = line.split(',')
        start_time = int(data_arr[0])/1000.0

        temp = data_arr[6]
        for i in range(7,len(data_arr)):
            temp += ',' + data_arr[i]
        
        dict_ = eval(temp)
        if start_time < (int(prev_start_time) + int(ux_time_win)):
            total_sessions += 1
            total_domains += len(dict_)
            total_bytes += int(data_arr[3])
            for domain in dict_:            
                try:
                    time_window_domain_dict[domain] += 1
                    # time_window_domain_dict[domain][0] += 1
                    # time_window_domain_dict[domain][1] += int(data_arr[3])
                except:
                    time_window_domain_dict[domain] = 1
                    # time_window_domain_dict[domain] = [1,int(data_arr[3])]
        else:
            total_unique_domains = len(time_window_domain_dict)
            for i in time_window_domain_dict:
                entropy += math.log2(time_window_domain_dict[i]/total_domains) * time_window_domain_dict[i]/total_domains

            entropy *= -1
            if total_domains:
                avg_bytes = total_bytes/total_domains
            else:
                avg_bytes = 0
            # vector = [len(time_window_domain_dict),total_domains, entropy, avg_bytes]
            vector = [total_unique_domains,total_domains, entropy, avg_bytes]
            #vector = [total_sessions, total_bytes/total_sessions , len(time_window_domain_dict), entropy]
            open('vectors/vectors_' + filename,'a').write(str(vector) + '\n')
            open('time/time_' + filename,'a').write(str(dt.fromtimestamp(prev_start_time)) + '\n')
            if create_database == 1:
                tw_freq_table.insert_one(freq_entry(id_,dt.fromtimestamp(prev_start_time).strftime('%Y-%m-%d %H:%M:%S'),vector,time_window_domain_dict,total_bytes),bypass_document_validation=True)
            id_ += 1
            total_bytes = 0
            entropy = 0
            total_domains = 0
            total_sessions = 0
            time_window_domain_dict = {}

            prev_start_time = int(prev_start_time) + int(ux_time_win)
            # while start_time >= int(prev_start_time) + int(ux_time_win):
            #     if total_domains:
            #         avg_bytes = total_bytes/total_domains
            #     else:
            #         avg_bytes = 0
            #     vector = [0,total_domains, entropy, avg_bytes]
            #     # open('vectors/vectors_' + filename,'a').write(str(vector) + '\n')
            #     # open('time/time_' + filename,'a').write(str(dt.fromtimestamp(prev_start_time)) + '\n')
            #     if create_database == 1:
            #         tw_freq_table.insert_one(freq_entry(id_,dt.fromtimestamp(prev_start_time).strftime('%Y-%m-%d %H:%M:%S'),vector,time_window_domain_dict,total_bytes),bypass_document_validation=True)
            #     id_ += 1
            #     prev_start_time = int(prev_start_time) + int(ux_time_win)

            total_sessions += 1
            total_domains += len(dict_)
            total_bytes += int(data_arr[3])
            for domain in dict_:            
                try:
                    time_window_domain_dict[domain] += 1
                    # time_window_domain_dict[domain][0] += 1
                    # time_window_domain_dict[domain][1] += int(data_arr[3])
                except:
                    time_window_domain_dict[domain] = 1
                    # time_window_domain_dict[domain] = [1,int(data_arr[3])]


    for i in time_window_domain_dict:
        entropy += math.log2(time_window_domain_dict[i]/total_domains) * time_window_domain_dict[i]/total_domains
    entropy *= -1
    # vector = [len(time_window_domain_dict),total_domains, entropy, total_bytes/total_sessions]
    vector = [len(time_window_domain_dict),total_domains, entropy, total_bytes/total_domains]
    open('vectors/vectors_' + filename,'a').write(str(vector))
    open('time/time_' + filename,'a').write(str(dt.fromtimestamp(prev_start_time)) + '\n')
    if create_database == 1:
        tw_freq_table.insert_one(freq_entry(id_,dt.fromtimestamp(prev_start_time).strftime('%Y-%m-%d %H:%M:%S'),vector,time_window_domain_dict,total_bytes),bypass_document_validation=True)
    id_ += 1



def stream(filename):
    lines = open("vectors/vectors_" + filename).read().split('\n')
    time = open('time/time_' + filename).read().split('\n')
    # open('result/result_' + filename,'w')    # uncomment this
    X = np.array([eval(line) for line in lines])

    # point_data = open("point_data.csv",'w')
    # point_data = open("point_data.csv",'a')
    count = 0
    count_with_zero = 0
    

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
    average_vector_non_zero = [0,0,0,0]
    # For each shingle...
    for index, point in enumerate(X):
        # For each tree in the forest...
        #print(point[0], point[1])
        average_vector[0] = (average_vector[0]*(index) + point[0])/(index + 1)
        average_vector[1] = (average_vector[1]*(index) + point[1])/(index + 1)
        average_vector[2] = (average_vector[2]*(index) + point[2])/(index + 1)
        average_vector[3] = (average_vector[3]*(index) + point[3])/(index + 1)

        if point[0] != 0:
            average_vector_non_zero[0] = (average_vector_non_zero[0]*(index) + point[0])/(index + 1)
            average_vector_non_zero[1] = (average_vector_non_zero[1]*(index) + point[1])/(index + 1)
            average_vector_non_zero[2] = (average_vector_non_zero[2]*(index) + point[2])/(index + 1)
            average_vector_non_zero[3] = (average_vector_non_zero[3]*(index) + point[3])/(index + 1)

        # if point[0] == 0:
        #     open('result_with_zero/result_with_zero_' + filename,'a').write( str(count_with_zero) + ',' + str(time_) + ',' + str(point) + ',' + str(0) + '\n')
        #     count_with_zero += 1
        #     continue

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
        time_ = time[ptr].split('.')[0]
        ptr += 1 
        #points = point.split(',')
        # open('result/result_' + filename,'a').write( str(count) + ',' + str(time_) + ',' + str(point) + ',' + str(avg_codisp[index]) + '\n')   # uncomment this
        
        # open('result_with_zero/result_with_zero_' + filename,'a').write( str(count_with_zero) + ',' + str(time_) + ',' + str(point) + ',' + str(avg_codisp[index]) + '\n')
        # count_with_zero += 1
        
        # total_windows = index
        if create_database == 1:
            result_table = MongoClient()[dbname][('result_data_' + str(filename).split('.')[2] + '_' + str(filename).split('.')[3])]
            tw_freq_table = MongoClient()[dbname][('tft_' + str(filename).split('.')[2] + '_' + str(filename).split('.')[3])]
            result_table.insert_one(entry(count,str(time_),str(point),float(avg_codisp[index])))
            # tw_freq_table.update_one({"Time" : dt.strptime(str(time_.split('.')[0]),"%Y-%m-%d %H:%M:%S")},{"$set" : update_freq_entry(float(avg_codisp[index]))})
            time_ = dt.strptime(time_,"%Y-%m-%d %H:%M:%S").timestamp()
            # time_ = dt.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
            tw_freq_table.update_one({"Time" : dt.fromtimestamp(time_).strftime('%Y-%m-%d %H:%M:%S')},{"$set" : update_freq_entry(float(avg_codisp[index]))})
    
        count += 1
        #if count > 10:
        #    break
        #print(str(point)[1:-1] + "  " + str(avg_codisp[index]))

    #print(avg_codisp)
    print(filename + ' => ' + str(average_vector))
    open('result_avg_vectors.csv','a').write(str(filename) + ',' + str(average_vector) + '\n')
    # print(filename + '_non_zero => ' + str(average_vector_non_zero))
    # open('result_avg_non_zero_vectors.csv','a').write(str(average_vector_non_zero) + '\n')
    id_ = 0
    if create_database == 1:
        # avg_vector_collections = MongoClient()[dbname][('avg_vectors')]
        # avg_vector_collections.insert_one(avg_vector_entry(id_,filename[:-4],str(average_vector)),bypass_document_validation=True)
        id_ = id_ + 1

    # import pandas as pd
    # import matplotlib.pyplot as plt
    # import seaborn as sns

    # fig, ax1 = plt.subplots(figsize=(10, 5))

    # color = 'tab:red'
    # ax1.set_ylabel('Data', color=color, size=14)
    # ax1.plot(X, color=color)
    # ax1.tick_params(axis='y', labelcolor=color, labelsize=12)
    # ax1.set_ylim(0,160)
    # ax2 = ax1.twinx()
    # color = 'tab:blue'
    # ax2.set_ylabel('CoDisp', color=color, size=14)
    # ax2.plot(pd.Series(avg_codisp), color=color)
    # ax2.tick_params(axis='y', labelcolor=color, labelsize=12)
    # ax2.grid('off')
    # ax2.set_ylim(0, 160)
    # plt.title('X with injected anomaly (red) and anomaly score (blue)', size=14)
    # plt.show()




import multiprocessing
import os


csv_files = [] 
for file in os.listdir('dpi_filtered_data/'):
    if '.csv' in file and '192.168.' in file:
        csv_files.append(file)

# csv_files.append('192.168.2.214.csv')
# csv_files.append('192.168.2.172.csv')
# csv_files.append('192.168.2.175.csv')
# csv_files.append('192.168.2.145.csv')
# csv_files.append('192.168.2.185.csv')
# csv_files.append('192.168.2.159.csv')
# print(csv_files)

# for file in csv_files:
#     p = multiprocessing.Process(target=analysis,args=(file,))
#     p.start()
#     p.join()
    

for file in csv_files:
    p = multiprocessing.Process(target=stream,args=(file,))
    p.start()
    p.join()

end_time = dt.now()
print("Time taken to execute the script is : " + str(end_time - start_time))