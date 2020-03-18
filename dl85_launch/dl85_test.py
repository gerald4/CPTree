#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:25:36 2020

@author: gnanfack
"""
import os
import pandas as pd




from sklearn.metrics import confusion_matrix

from sklearn.metrics import accuracy_score
import time
import argparse

import dl85
from dl85 import DL85Classifier


#This code is based on https://dl85.readthedocs.io/en/latest/auto_examples/plot_classifier_iterative_c_plus.html

dataname = ["balance_scale", "banknote_authentication", "biodeg", "car", "credit_approval", "hepatitis",
 		   "ionosphere", "iris", "mammographic_masses", "monk1", "monk2", "monk3", "pima_indian_diabetes",
 		   "post_operative_patient", "seismic", "spambase", "spect_heart", "thoracy_surgery", "tic_tac_toe",
 		   "wine"]
evaluation_method = "cat_dis_holdout"

parser = argparse.ArgumentParser(description='Parameters')

parser.add_argument('--dataset_name', help="the name of the dataset", default="car")



parser.add_argument('--L', help="number of leaf nodes", type=int, default=6)
parser.add_argument('--K', help="maximum depth", type=int, default=3)
parser.add_argument("--max_time",help="maximum time", type=int, default=600)
parser.add_argument("--iter",help="iteration", type=int, default=0)


args = parser.parse_args()



l=args.L
k=args.K
max_time=args.max_time
dataset=args.dataset_name
step=args.iter





path_train = '../dataset_benchmark/'+dataset+'/'+dataset+'_cat_dis_holdout_train_'+str(step)+'.csv'
path_test = '../dataset_benchmark/'+dataset+'/'+dataset+'_cat_dis_holdout_test_'+str(step)+'.csv'
if dataset in ["monk1", "monk2", "monk3", "spect_heart"] and step>=2:
	pass
else:
	data_train = pd.DataFrame(pd.read_csv(path_train, sep=";"))
	data_test = pd.DataFrame(pd.read_csv(path_test, sep=";"))

	X_train = data_train.values[:, :-1]
	y_train = data_train.values[:, -1]
	X_test = data_test.values[:, :-1]
	y_test = data_test.values[:, -1]
	filepath = f'../dataset_benchmark/{dataset}/DL85_{evaluation_method}_{dataset}.csv'
	clf = DL85Classifier(max_depth=k, iterative=True, time_limit=max_time)
	start = time.perf_counter()
	print("Model building...", dataset)
	clf.fit(X_train, y_train)
	duration = time.perf_counter() - start
	print("Model built. Duration of building =", round(duration, 4))
	y_pred = clf.predict(X_test)
	print("Confusion Matrix below")
	train_accuracy = round(clf.accuracy_, 4)
	test_accuracy= round(accuracy_score(y_test, y_pred), 4)
	print("Accuracy DL8.5 on test set =", round(accuracy_score(y_test, y_pred), 4))
	mode = 'a' if os.path.exists(filepath) else 'w'
	with open(filepath, mode) as f:
		if f.tell()==0:
			f.write("dataset_name,step, time_taken,K,dl8.5_train,dl8.5_test\n"+dataset+","+str(step)+","+str( round(duration, 4)/60)+","+str(k)+","+str(train_accuracy)+","+str(test_accuracy)+"\n")
		else:
			f.write(dataset+","+str(step)+","+str( round(duration, 4)/60)+","+str(k)+","+str(train_accuracy)+","+str(test_accuracy)+"\n")
