import os
import pandas as pd
import numpy as np
import csv
import shutil
from datetime import datetime
import time
from tqdm import tqdm
import re

# if os.path.exists("Analysis/accuracy.csv"):
#     creation_time = os.path.getctime("Analysis/output.csv")
#     creation_dt = datetime.fromtimestamp(creation_time)
#     dt = creation_dt.strftime('%Y_%m_%d')

#     shutil.move("Analysis/accuracy.csv", "Analysis/old_accuracy/accuracy_" + str(dt) + ".csv")

# if os.path.exists(os.path.join(os.getcwd(),"Analysis/output.csv")):
#     creation_time = os.path.getctime("Analysis/output.csv")
#     creation_dt = datetime.fromtimestamp(creation_time)
#     dt = creation_dt.strftime('%Y_%m_%d')

#     shutil.move("Analysis/output.csv", "Analysis/old_output/output_" + str(dt) + ".csv")

acc = pd.DataFrame()

output = pd.DataFrame() 

# grads = pd.read_csv('Analysis/coords.csv')

mDES = []
acc_data = []

for file in tqdm(os.listdir("Tasks/log_file")):

    acc_dict = {}
    
    ftemp = file.split('.')[0]

    if not 'full' in ftemp.split('_'):

        _,_,subject,seed = ftemp.split("_")
        subject = "subject_"+str(int(re.findall(r'\d+', subject)[0]))


        sub_df = pd.read_csv(os.path.join("Tasks\\log_file",file), skiprows=4)

        acc_dict["subject_id"] = subject

        line_dict = {}
        enum = 0
        for index, row in sub_df.iterrows():

            line_dict["subject_id"] = subject

            if row['Timepoint'] == 'Runtime Mod':
                line_dict["Runtime_mod"] = row[1]
                prev_run = row[1]

            elif row['Timepoint'] == 'ESQ':
                enum += 1

                task_name = row['Assoc Task']
                if task_name == "Movie Task-Movie Task-bridge":
                    task_name = "Movie Task bridge"
                line_dict["Task_name"] = task_name.replace(" ","_")

                if float(row['Experience Sampling Response']) >= 1 :
                    line_dict[row['Experience Sampling Question']]=row['Experience Sampling Response']
                else:
                    line_dict[row['Experience Sampling Question']]=np.nan

            if enum == 16:
                if float(row['Experience Sampling Response']) >= 1 :
                    line_dict[row['Experience Sampling Question']]=row['Experience Sampling Response']
                else:
                    line_dict[row['Experience Sampling Question']]=np.nan

                enum = 0
                mDES.append(line_dict)

                line_dict = {'Runtime_mod':prev_run}

    else:
        sub_df = pd.read_csv(os.path.join("Tasks\\log_file",file), skiprows=4)
        print('pause')

test_df = pd.DataFrame(mDES)
print('poop?')



            # if task_name == "Movie Task-Movie Task-incept":
            #     task_name = "Movie Task-incept"
            #     line_dict["Task_name"] = task_name.replace(" ","_")
            # grads = graddict[line_dict["Task_name"]]
            # line_dict["Gradient 1"],line_dict["Gradient 2"],line_dict["Gradient 3"],line_dict["Gradient 4"],line_dict["Gradient 5"] = grads
                
                # with open("Analysis/output.csv", 'a', newline="") as outf:
                #     wr = csv.writer(outf)
                #     #wr.writerow(list(line_dict.keys()))
                #     wr.writerow(list(line_dict.values()))
            #     task_name = row[10]
            #     if float(row[4]) >= 1 :
            #         line_dict[row[3]]=row[4]
            #     else :
            #         line_dict[row[3]] = np.nan
            #     line_dict["Task_name"] = task_name.replace(" ","_")
            # ##print(row)



def sortingfunction(exp,row,resps):
    global prevtime
    global en
    # if exp == "Reading_Task":
    #     # Collect no data
    #     pass
    if exp == "Experience_Sampling_Questions":
        # Collect response time
        if row[3].split("_")[1] == "start":
            prevtime = float(row[1])
        elif row[3].split("_")[1] == "response":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        pass

    if exp == "Memory_Task":
        # Collect no data
        pass

    if exp == "GoNoGo_Task":
        # Collect response time, % correct
        try:
            # Resp time
            if row[0].split(" ")[1] == "start":
                prevtime = float(row[1])
            elif row[0].split(" ")[1] == "end":
                resptime = float(row[1]) - prevtime  
                resps[exp]["Response_Time"].append(resptime)
            # Accuracy
            if row[2] != '':
                if row[2] == 'noResponse':
                    if row[9] == 'Type: Go':
                        resps[exp]["Accuracy_Go"].append(False)
                if row[2].upper() == 'FALSE':
                    if row[9] == 'Type: Go':
                        resps[exp]["Accuracy_Go"].append(True)
                if row[2].upper() == 'FALSE':
                    if row[9] == 'Type: NoGo':
                        resps[exp]["Accuracy_NoGo"].append(False)
                if row[2].upper() == 'TRUE':
                    if row[9] == 'Type: NoGo':
                        resps[exp]["Accuracy_NoGo"].append(True)
        except Exception as e:
            #print(e)
            pass
        pass

    if exp == "Hard_Math_Task":
        #print(row)
        if row[0] == 'Choice presented':
            prevtime = float(row[1])
        elif row[0] == 'Choice made':
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response_Time"].append(resptime)
        # Collect response time, % correct
        if row[0] == 'Math Trial End':
            if not "en" in globals():
                
                en = 0
            if en == 0:
                en = 1
                if row[2].upper() == "TRUE":
                    resps[exp]["Accuracy"].append(True)
                elif row[2].upper() == "FALSE":
                    resps[exp]["Accuracy"].append(False)
                else:
                    return 1/0
            elif en == 1:
                en = 0
            
        pass

    pass