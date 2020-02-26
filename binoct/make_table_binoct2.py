#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 13:46:00 2020

@author: gnanfack
"""

import os


datasets =["balance_scale", "banknote_authentication", "biodeg", "car", "credit_approval", "hepatitis",
 		   "ionosphere", "iris", "mammographic_masses", "monk1", "monk2", "monk3", "pima_indian_diabetes",
 		   "post_operative_patient", "seismic", "spambase", "spect_heart", "thoracy_surgery", "tic_tac_toe",
 		   "wine"]

evaluation_method = "cat_num"

forest_bounds = -1
inputstart = 0
count_max = -1
for step in range(1,6):
#for filename in glob.glob(os.path.join(path1, '*.train*.csv')):
    for dataset in datasets:
        if dataset in ["monk1", "monk2", "monk3", "spect_heart"] and step>=2:
            pass
        else:

            filename=f"../dataset_benchmark/{dataset}/{dataset}_{evaluation_method}_train_"+str(step)+".csv"

            filepath = f'../dataset_benchmark/{dataset}/binoct_{evaluation_method}_{dataset}.csv'
		     #lcb.main(["-f",filename, "-d", 1, "-t", 900, "-p", 300])

            for depth in range(2,5):
                k = depth
                l = 2**k
                pythonfile = f"{dataset}_{evaluation_method}_train_{step}.csv-{depth}-{count_max}-{forest_bounds}-{inputstart}.sol.py"
                os.system(f"cd ../dataset_benchmark/{dataset}; python3 {pythonfile}; cd ../../binoct/")

                accuracy_train_file = f"../dataset_benchmark/{dataset}/{pythonfile}-{dataset}_{evaluation_method}_train_{step}.csv.result.txt"
                binoct_train_acc = 0

                accuracy_test_file = f"../dataset_benchmark/{dataset}/{pythonfile}-{dataset}_{evaluation_method}_test_{step}.csv.result.txt"
                binoct_test_acc = 0
                with open(accuracy_train_file, "r") as f:
                     binoct_train_acc = f.read().split('crosstable')[0].split()[1]
                with open(accuracy_test_file, "r") as f:
                     binoct_test_acc = f.read().split('crosstable')[0].split()[1]
                     print(binoct_test_acc)

                mode = 'a' if os.path.exists(filepath) else 'w'
                with open(filepath, mode) as f:
                    if f.tell()==0:
                         f.write("dataset_name,step, L, K, binoct_train,binoct_test\n"+dataset+","+str(step)+","+str(l)+","+str(k)+","+str(binoct_train_acc)+","+str(binoct_test_acc)+"\n")
                    else:
                         f.write(dataset+","+str(step)+","+str(l)+","+str(k)+","+str(binoct_train_acc)+","+str(binoct_test_acc)+"\n")

					#p = subprocess.Popen([f"python3 {pythonfile}"], cwd=f"../dataset_benchmark/{dataset}/")


