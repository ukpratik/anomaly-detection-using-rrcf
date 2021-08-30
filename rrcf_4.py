import json
import os
import sys
import math

base = 10
#dir_path = sys.argv[1]
count = 0

all_files = []
dir_path = "/var/log/vehere/dpi/dpi/"
open("usr_data_new_database.csv","a")
#FILTER_IP = "192.168.2.201"

#open("usr_data_new_database.csv",'a').write(' Time, Duration, Source IP, Total Bytes, Entropy, Total Domiains\n')
done_files = open("done_files.txt","r").read().split('\n')

suffix_list = set(open('public_suffix_list.dat','r').read().split('\n'))
def suffix(domain):
    parts = domain.split('.')
    l = len(parts)
    temp_suffix = parts[l - 1]
    for i in range(l-1):
        if (parts[l - i -1] + '.' + temp_suffix) in suffix_list:
            temp_suffix = parts[l - i -1] + '.' + temp_suffix
        else:
            return temp_suffix
    return temp_suffix

for file_ in os.listdir(dir_path):
    #if (dir_path + file_) in user_data_done_files:
        #continue
    if file_[-5:] == ".json":
        if dir_path + file_ in done_files:
            continue
        all_files.append(dir_path + file_)
        #print(dir_path + file_)

files_here = os.listdir()

for file_ in all_files:
#    if count > 40000:
#        break
    try:
        flines = open(file_,'r').read().split('\n')
 #       print(" ----------- Step 2B  -----------")
    except:
        continue
    for line in flines:
        # print(" ----------- Step 2C  -----------")
        #print(line)
        try:
            json_data = json.loads(line)
            #print(" ----------- Step 2D  -----------")
        except:
            continue
        domain = ""
        dnsheaders = []

        try:
            dnsdomainnames = json_data["payload"]["dns_domain_names"]
        except:
            continue
        
        dict_ = {}
        total_domains = 0
        for e in dnsdomainnames:
            print(suffix(e))
            try:
                dict_[e] += 1
            except:
                dict_[e] = 1
            total_domains += 1

        entropy = 0
        if total_domains != 0:
            for i in dict_:
                entropy += math.log2(dict_[i]/total_domains) * dict_[i]/total_domains
      
        entropy *= -1

        num_of_periods = len(domain.split('.'))
        time = json_data["session"]["start_time"]
        duration = json_data["session"]["duration"]
        src_ip = json_data["network"]["src_ip"]
        #dst_ip = json_data["network"]["dst_ip"]

        #print(str(num_of_periods) + "  "  + str(time_hour) + " " + json_data["network"]["src_ip"] )
 
        json_haddix = json_data["network"]["src_ip"] # Json Haddix :)
        if json_haddix.split('.')[0] == "192":
            src_ip = json_data["network"]["src_ip"]
            # if json_haddix != FILTER_IP:
            #     continue
            #print(" ----------- Step 3B  -----------")
            if (str(src_ip) + '.csv') in files_here:
                open(str(src_ip) + '.csv','a').write(str(time) + ',' + str(duration) + "," + str(src_ip)  + "," + str(json_data["session"]["total_bytes"]) + ',' + str(entropy) + ',' + str(total_domains) + ',' + str(dict_) + '\n')
            else:
                open(str(src_ip) + '.csv','w').write(str(time) + ',' + str(duration) + "," + str(src_ip)  + "," + str(json_data["session"]["total_bytes"]) + ',' + str(entropy) + ',' + str(total_domains) + ',' + str(dict_) + '\n')
                files_here.append(str(src_ip) + '.csv')
        else:
            #print("[ Else ] Escaped if condn : Continued")
            continue

        

        #open("usr_data.csv","a").write(str(time_hour) + " " + src_ip + " " + domain + " tb_"+ str(json_data["session"]["total_bytes"]) + " " + Query_popularity + " " + str(num_of_periods) + '\n')
#        open("usr_data_new_database.csv",'a').write(str(time) + ',' + str(duration) + "," + str(src_ip) + "," + str(dict_) + ",tb_" + str(json_data["session"]["total_bytes"]) + '\n')
        #open("usr_data_new_database.csv",'a').write(str(time) + ',' + str(duration) + "," + str(src_ip)  + "," + str(json_data["session"]["total_bytes"]) + ',' + str(entropy) + ',' + str(total_domains) + ',' + str(dict_) + '\n')
        count += 1
    open('done_files.txt', 'a').write(file_ + '\n')

