from datetime import datetime
import math
from time import strptime
from pymongo import MongoClient
import matplotlib.pyplot as plt
import json

while 1:
    ip = input("Enter Machine IP : ")

    start_time = input("Enter Start time : ")
    end_time = input("Enter End time : ")

    num_of_queries = 500

    if ip == '':
        ip = prev_ip
    prev_ip = ip

    if start_time == '':
        start_time = "2021-05-24 15:07:21"

    if end_time == '':
        end_time = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S").timestamp() + 300*num_of_queries

    dbname = "rrcf_beta_4"

    tw_freq_table = MongoClient()[dbname][('tft_' + str(ip).split('.')[2] + '_' + str(ip).split('.')[3])]

    my_query = {'$and' : [{"Time" : { "$gte" : str(datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")) } } , {"Time" : { "$lte" : str(datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"))}}]}

    result_data = tw_freq_table.find(my_query)

    count = 0
    for x in result_data:
        if count > 20:
            break
        print(x)
        print('\n') 
        count += 1

    plot_id = int(input("Plot for ID : "))
    if (plot_id == ''):
        continue

    detail_query = {"_id" : plot_id}                   # ,{'_id': 1, 'Time': 1, 'Vector': 0, 'Dict': 1, 'Total bytes': 0}
    domain_data = tw_freq_table.find_one(detail_query)

    # domain_data = list(domain_data)

    # json_data = dumps(domain_data)
    # print(domain_data)
    # for d in domain_data:
    #     json_data = dumps(d)
    #     print(json_data[3])
        
    data = str(domain_data).replace("'",'"')
    # print(data)
    data = json.loads(data)
    # print(data)
    # print(data["Dict"])
    domain_json = json.loads(str(data["Dict"]).replace("'",'"'))
    # print(domain_json)
    x = []
    y = []
    for d in eval(str(data["Dict"])):
        y.append(d)
        x.append(domain_json[d])


    plt.barh(y,x,color='green',height=0.1)
    plt.xlabel("Frequency")
    plt.ylabel("Domains")
    
    plt.title(" Machine_IP : " + str(ip) + "\n Anomaly_Score: " + str(data['Average Codisp']) + "\n Time_Window: " + str(data['Time']) + '\n [Unique_Domains, Total_Domains, Entropy, Average_Bytes] = ' + str(data["Vector"]) )
    plt.show()