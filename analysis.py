import math
import os
import sys
from datetime import datetime as dt

#os.system("python3 rrcf_3.py")
#os.system("python3 rearrange_file.py")

import pymongo
from pymongo import MongoClient
# tw_freq_table = MongoClient().rrcf_beta.tft3 #timeWindow_freq_table
id_ = 0
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


filename = sys.argv[1]
lines = open(filename,'r').read().split('\n')

#  Time, Duration, Source IP, Total Bytes, Entropy, Total Domains, Dictionary
#   0  ,   1     ,  2       ,  3         , 4      ,    5         ,     6


prev_start_time =  int(lines[1].split(',')[0])/1000.0   # millisseconds to seconds
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
    # else:
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
        for i in time_window_domain_dict:
            entropy += math.log2(time_window_domain_dict[i]/total_domains) * time_window_domain_dict[i]/total_domains

        entropy *= -1
        if total_sessions:
            avg_bytes = total_bytes/total_sessions
        else:
            avg_bytes = 0
        vector = [len(time_window_domain_dict),total_domains, entropy, avg_bytes]
        #vector = [total_sessions, total_bytes/total_sessions , len(time_window_domain_dict), entropy]
        open('vectors/vectors_' + filename,'a').write(str(vector) + '\n')
        open('time/time_' + filename,'a').write(str(dt.fromtimestamp(prev_start_time)) + '\n')
        # tw_freq_table.insert_one(freq_entry(id_,str(dt.fromtimestamp(prev_start_time)),vector,time_window_domain_dict,total_bytes),bypass_document_validation=True)
        id_ += 1
        total_bytes = 0
        entropy = 0
        total_domains = 0
        total_sessions = 0
        time_window_domain_dict = {}

        prev_start_time = int(prev_start_time) + ux_time_win
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
vector = [len(time_window_domain_dict),total_domains, entropy, total_bytes/total_sessions]
open('vectors/vectors_' + filename,'a').write(str(vector))
open('time/time_' + filename,'a').write(str(dt.fromtimestamp(prev_start_time)) + '\n')
# tw_freq_table.insert_one(freq_entry(id_,str(dt.fromtimestamp(prev_start_time)),vector,time_window_domain_dict,total_bytes),bypass_document_validation=True)
id_ += 1