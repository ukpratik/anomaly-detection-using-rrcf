import datetime
import sys
import matplotlib.pyplot as plt
import os

files = []
start_time = 0
end_time = 1000
# print(sys.argv)
# print(len(sys.argv))
specific = 0

colors = ['black', 'dimgray', 'dimgrey', 'gray', 'grey', 'darkgray', 'darkgrey', 'silver', 'lightgray', 'lightgrey', 'gainsboro', 'whitesmoke', 'white', 'snow', 'rosybrown', 'lightcoral', 'indianred', 'brown', 'firebrick', 'maroon', 'darkred', 'red', 'mistyrose', 'salmon', 'tomato', 'darksalmon', 'coral', 'orangered', 'lightsalmon', 'sienna', 'seashell', 'chocolate', 'saddlebrown', 'sandybrown', 'peachpuff', 'peru', 'linen', 'bisque', 'darkorange', 'burlywood', 'antiquewhite', 'tan', 'navajowhite', 'blanchedalmond', 'papayawhip', 'moccasin', 'orange', 'wheat', 'oldlace', 'floralwhite', 'darkgoldenrod', 'goldenrod', 'cornsilk', 'gold', 'lemonchiffon', 'khaki', 'palegoldenrod', 'darkkhaki', 'ivory', 'beige', 'lightyellow', 'lightgoldenrodyellow', 'olive', 'yellow', 'olivedrab', 'yellowgreen', 'darkolivegreen', 'greenyellow', 'chartreuse', 'lawngreen', 'honeydew', 'darkseagreen', 'palegreen', 'lightgreen', 'forestgreen', 'limegreen', 'darkgreen', 'green', 'lime', 'seagreen', 'mediumseagreen', 'springgreen', 'mintcream', 'mediumspringgreen', 'mediumaquamarine', 'aquamarine', 'turquoise', 'lightseagreen', 'mediumturquoise', 'azure', 'lightcyan', 'paleturquoise', 'darkslategray', 'darkslategrey', 'teal', 'darkcyan', 'aqua', 'cyan', 'darkturquoise', 'cadetblue', 'powderblue', 'lightblue', 'deepskyblue', 'skyblue', 'lightskyblue', 'steelblue', 'aliceblue', 'dodgerblue', 'lightslategray', 'lightslategrey', 'slategray', 'slategrey', 'lightsteelblue', 'cornflowerblue', 'royalblue', 'ghostwhite', 'lavender', 'midnightblue', 'navy', 'darkblue', 'mediumblue', 'blue', 'slateblue', 'darkslateblue', 'mediumslateblue', 'mediumpurple', 'rebeccapurple', 'blueviolet', 'indigo', 'darkorchid', 'darkviolet', 'mediumorchid', 'thistle', 'plum', 'violet', 'purple', 'darkmagenta', 'fuchsia', 'magenta', 'orchid', 'mediumvioletred', 'deeppink', 'hotpink', 'lavenderblush', 'palevioletred', 'crimson', 'pink', 'lightpink']

rgb_colors = []
i = 0
j = 0
k = 0
# while i <= 1:
#     j = 0
#     while j <= 1:
#         k = 0
#         while k <= 1:
#             rgb_colors.append(tuple((i,j,k)))
#             k += 0.1
#         j += 0.1
#     i += 0.1

# print(len(rgb_colors))

# print(files)

start_flg = 1
if len(sys.argv) > 1:
    specific = 1
    for i in range(0,len(sys.argv)-1):
        files.append(sys.argv[i+1])
else:
    for file in os.listdir('result/'):
        if len(file) < 4:
            continue
        files.append(file[7:-4])

title = ''

for i in range(0,len(files)):
    if len(files[i]) < 4:
        continue
    # print(files[i])
    data = open('result/result_' + files[i] + '.csv','r').read().split('\n')

    x = []
    y = []

    for d in data:
        d = d.split(',')
        if len(d) < 2 :
            continue
        # id_ = d[0]
        time = d[1].split('.')[0]
        time = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")

        #############################################################################################################################################
        # if start_flg == 0:
        #     # current_time = datetime.datetime.timestamp(datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S'))
        #     new_time = datetime.datetime.timestamp(datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S'))   # changing to unix time
        #     print(new_time)
        #     while new_time != (prev_time + 300):
        #         temp_time = datetime.datetime.fromtimestamp(prev_time + 300).strftime('%Y-%m-%d %H:%M:%S')  # chnage to normal timestamp
        #         x.append(temp_time)
        #         y.append(float(0))
        #         # new_time = prev_time
        #         prev_time = prev_time + 300
        #         print(temp_time)
        #         print(prev_time)
            
        # time = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
        # prev_time = datetime.datetime.timestamp(time)
        # print(time)
        # print(prev_time)
        #############################################################################################################################################

        avg_codisp = d[3]
        # x.append(int(id_))
        x.append(time)
        y.append(float(avg_codisp))
        if start_flg == 1:
            start_flg = 0

    # print(x)
    # print(y)
    # plt.plot(x[start_time:end_time],y[start_time:end_time])
    # plt.plot(x[start_time:end_time],y[start_time:end_time], color =colors[i])
    # plt.scatter(x[start_time:end_time],y[start_time:end_time], color =colors[i],s=1.5)

    plt.bar(x[start_time:end_time],y[start_time:end_time], color =colors[j],width=0.001)
    # plt.scatter(x[start_time:end_time],y[start_time:end_time], color=colors[i],alpha=1,s=5) # (i + 0.1, i + 0.1, i + 0.1)

    # plt.plot(x[start_time:end_time],y[start_time:end_time], color =colors[i])
    # plt.plot(x[start_time:end_time],y[start_time:end_time], color ='tab:orange')
    title += str(files[i]) + ":" + str(colors[j]) + ',  '
    print(str(x[0]) + ' : ' + str(files[i]) + " : " + str(colors[j]))
    j += 3
    if i > 45:
        break
plt.xlabel("Time ->")
plt.ylabel("Anomaly Score ->")
plt.title(title)
plt.show()
