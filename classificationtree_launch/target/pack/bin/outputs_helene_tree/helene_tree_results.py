#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:05:53 2020

@author: gnanfack
"""

import os
import pandas as pd


datasets =['banknote_authentication', 'biodeg', 'credit_approval','hepatitis', 'ionosphere', 'mammographic_masses',
		   'monk1', 'monk2', 'monk3', 'pima_indian_diabetes', 'ionosphere', 'seismic', 'spambase', 'spect_heart', 'thoracy_surgery',
		    'tic_tac_toe']

evaluation_method = "cat_dis_holdout"


for step in range(1,6):
#for filename in glob.glob(os.path.join(path1, '*.train*.csv')):
	for dataset in datasets:
		if dataset in ["monk1", "monk2", "monk3", "spect_heart"] and step>=2:
			pass
		else:

			filename=f"../../../../../dataset_benchmark/{dataset}/{dataset}_{evaluation_method}_train_"+str(step)+".csv"

			data_train = pd.DataFrame(pd.read_csv(filename, sep=";"))
			filepath = f'../../../../../dataset_benchmark/{dataset}/Helenetree_{evaluation_method}_{dataset}.csv'
		     #lcb.main(["-f",filename, "-d", 1, "-t", 900, "-p", 300])

			for depth in range(2,5):
				k = depth
				l = 0
				resultfile = f"{dataset}_cat_dis_holdout_results_helene_iter={step}_depth={depth}.txt"
				results = []
				with open(resultfile) as f:
					results = f.readlines()
				if len(results)>=11:
					helene_test_acc = float(results[10].split(":")[1])
					helene_train_acc = 1 - float(results[2].split(":")[1])/data_train.shape[0]


					mode = 'a' if os.path.exists(filepath) else 'w'
					with open(filepath, mode) as f:
						if f.tell()==0:
							f.write("dataset_name,step,L,K,HeleneTree_train,HeleneTree_test\n"+dataset+","+str(step)+","+str(l)+","+str(k)+","+str(helene_train_acc)+","+str(helene_test_acc)+"\n")
						else:
							f.write(dataset+","+str(step)+","+str(l)+","+str(k)+","+str(helene_train_acc)+","+str(helene_test_acc)+"\n")
				else:
					print(dataset,depth)

