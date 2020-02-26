#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:46:49 2020

@author: gnanfack
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import KBinsDiscretizer


def cat_to_bin(dataset, categorical_features):
	data = dataset.loc[:,:]
	for att in categorical_features:
	    dm1 = pd.get_dummies(data[att], drop_first = False, prefix = att)
	    data = data.drop(att, axis = 1)

	    data = pd.concat([data, dm1], axis = 1)

	return data

def cat_to_bin_encoding(data_train, data_test, categorical_features):

	data = cat_to_bin(data_train.append(data_test), categorical_features)

	return data.iloc[:data_train.shape[0]], data.iloc[data_train.shape[0]:]



def num_to_cat(X_train, X_test, numerical_features, number_bins = 3):

	data = X_train.values
	enc=KBinsDiscretizer(n_bins = number_bins, encode = 'ordinal', strategy = 'quantile')
	enc.fit(data)
	X = enc.transform(data)

	datatrain = pd.DataFrame(X,columns=numerical_features)

	datatest = pd.DataFrame(enc.transform(X_test.values), columns=numerical_features)

	return datatrain, datatest


def train_val_test(data, list_classes, folder_name, numerical_features, categorical_features,
				   dataset_name, use_classes=False, data2=pd.DataFrame(), nfolds = 5, bins=3):

	X_test = None
	y_test = None

# =============================================================================
# 	list_data_cont_train = []
# 	list_data_cont_test = []
#
# 	list_data_dist_train = []
# 	list_data_dist_test = []
#
# 	list_data_dist_val = []
# =============================================================================
	#Preprocessing dataset
	Y = data['class']
	X = data.drop('class',axis=1)
	X = cat_to_bin(dataset = X, categorical_features = categorical_features)
	le = LabelEncoder()
	le.fit(Y)
	print(le.classes_)
	Y = pd.DataFrame(le.transform(Y), columns=['class'])

	if not(data2.empty):
		y_test = le.transform(data2['class'])
		y_test = pd.DataFrame(le.transform(y_test), columns=['class'])
		X_test = data2.drop('class', axis=1)
		X_test = cat_to_bin(dataset = X_test, categorical_features = categorical_features)


		nfolds = 1

		X_train = X
		y_train = Y

	for i in range(1, nfolds+1):
		if data2.empty:
			X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, stratify=Y, random_state = i)
		print('Debug: ','shape Train, Test : ', X_train.shape, X_test.shape)
		pd.concat([X_train, y_train], axis = 1, ignore_index = True).to_csv(folder_name+dataset_name+"_"+"cat_num_train_"+str(i)+".csv", index = False, sep = ";")

		pd.concat([X_test, y_test], axis = 1, ignore_index = True).to_csv(folder_name+dataset_name+"_"+"cat_num_test_"+str(i)+".csv", index = False, sep = ";")

		#Numerical features to categorical one
		if len(numerical_features) != 0:
			num_train = X_train[numerical_features]
			num_test = X_test[numerical_features]


			# Numeric to Categorical
			temp1, temp2 = num_to_cat(num_train, num_test, numerical_features, bins)
			temp1.index = X_train.index
			temp2.index = X_test.index

			X_train.update(temp1)
			X_test.update(temp2)
			#Categorical to binary
			x_train_num, x_test_num = cat_to_bin_encoding(data_train = X_train[numerical_features], data_test = X_test[numerical_features], categorical_features= numerical_features)
			print(x_train_num.shape)

			x_train_num.index = X_train.index
			x_test_num.index = X_test.index

			X_train = pd.concat([X_train, x_train_num], axis = 1)
			X_test = pd.concat([X_test, x_test_num], axis = 1)

			X_train = X_train.drop(numerical_features, axis =1)
			X_test = X_test.drop(numerical_features, axis =1)


		pd.concat([X_train, y_train], axis = 1).to_csv(folder_name+dataset_name+"_"+"cat_dis_holdout_train_"+str(i)+".csv", index = False, sep = ";")
		X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.33, stratify=y_train, random_state = 7)

		print('Debug: ','shape Train, Val : ',X_train.shape, X_val.shape)
		pd.concat([X_train, y_train], axis = 1).to_csv(folder_name+dataset_name+"_"+"cat_dis_crossval_train_"+str(i)+".csv", index = False, sep = ";")
		pd.concat([X_test, y_test], axis = 1).to_csv(folder_name+dataset_name+"_"+"cat_dis_holdout_test_"+str(i)+".csv", index = False, sep = ";")
		pd.concat([X_val, y_val], axis = 1).to_csv(folder_name+dataset_name+"_"+"cat_dis_crossval_val_"+str(i)+".csv", index = False, sep = ";")


# =============================================================================
# 	X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, stratify=y_train)
#
#
# 	C=np.unique(y_train)
# 	if use_classes:
# 		C=np.unique(list_classes)
# 	lb=LabelBinarizer()
# 	#lb.fit(C)
# 	lb.fit(C)
# 	y_train_ohot=lb.transform(y_train)
# 	y_val_ohot=lb.transform(y_val)
# 	y_test_ohot=lb.transform(y_test)
# 	if len(C)==2:
# 		y_train_ohot= np.hstack((1-y_train_ohot, y_train_ohot))
# 		y_test_ohot= np.hstack((1-y_test_ohot, y_test_ohot))
# 		y_val_ohot= np.hstack((1-y_val_ohot, y_val_ohot))
#
# 	N=X_train.shape[0]
# 	M=X_train.shape[1]
#
# 	return N, M, X_train, X_val, X_test, y_train, y_val, y_test, y_train_ohot, y_val_ohot, y_test_ohot, list_classes,l_dataset
# =============================================================================


def  read_car_evaluation(path="dataset_benchmark/car/car.data", path_test=None):
	dataset=pd.read_table(path,delimiter=',',names=["buying","maint","doors","persons","lug_boot","safety","class"])


	mutiva_att=['buying','maint','doors','persons','lug_boot','safety']
	train_val_test(data = dataset, list_classes = ["unacc", "acc", "good", "vgood"],
				folder_name = "dataset_benchmark/car/", numerical_features = [],
				categorical_features = mutiva_att,
				dataset_name = "car", use_classes = False)

def read_balance_scale(path="dataset_benchmark/balance_scale/balance-scale.data", path_test=None):
	dataset=pd.read_table(path, delimiter=",",
            names=["class","Left-Weight","Left-Distance","Right-Weight","Right-Distance"])
#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)

	mutiva_att=["Left-Weight","Left-Distance","Right-Weight","Right-Distance"]


	train_val_test(data = dataset, list_classes =['Survived','Died'],
				folder_name = "dataset_benchmark/balance_scale/", numerical_features = [],
				categorical_features = mutiva_att,
				dataset_name = "balance_scale", use_classes = False)


def read_tic_tac_toe(path="dataset_benchmark/tic_tac_toe/tic-tac-toe.data", path_test=None):
	dataset=pd.read_table(path,delimiter=',',
	            names=["top-left-square","top-middle-square","top-right-square","middle-left-square","middle-middle-square","middle-right-square","bottom-left-square","bottom-middle-square","bottom-right-square","class"])
	#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)

	mutiva_att=["top-left-square","top-middle-square","top-right-square","middle-left-square","middle-middle-square","middle-right-square","bottom-left-square","bottom-middle-square","bottom-right-square"]


	train_val_test(data = dataset, list_classes = ["positive", "negative"],
				folder_name = "dataset_benchmark/tic_tac_toe/", numerical_features = [],
				categorical_features = mutiva_att,
				dataset_name = "tic_tac_toe", use_classes = False)



def read_iris(path="dataset_benchmark/iris/iris.data", path_test=None):
	dataset=pd.read_csv(path,na_values='?',
            names=['Sepal_length',"Sepal_width","Petal_length","Petal_width","class"])

	train_val_test(data = dataset, list_classes = ["positive", "negative"],
				folder_name = "dataset_benchmark/iris/", categorical_features = [],
				numerical_features = ['Sepal_length',"Sepal_width","Petal_length","Petal_width"],
				dataset_name = "iris", use_classes = False)


def read_monk1(path="dataset_benchmark/monk1/monks-1.train",path_test="dataset_benchmark/monk1/monks-1.test"):
	dataset=pd.read_csv(path,na_values='?',sep=" ",names=['class','a1','a2','a3','a4','a5','a6','Id'])
#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)

	dataset2 = pd.read_csv(path_test,na_values='?',sep=" ",names=['class','a1','a2','a3','a4','a5','a6','Id'])

	dataset = dataset.drop("Id",axis=1)
	dataset2 = dataset2.drop("Id",axis=1)

	dataset = dataset.reset_index(drop=True)
	dataset2 = dataset2.reset_index(drop=True)


	train_val_test(data = dataset, data2 = dataset2, list_classes = ["0", "1"],
				folder_name = "dataset_benchmark/monk1/", categorical_features = [att for att in list(dataset) if att!='class'],
				numerical_features = [],
				dataset_name = "monk1", use_classes = False)

def read_monk2(path="dataset_benchmark/monk2/monks-2.train",path_test="dataset_benchmark/monk2/monks-2.test"):
	dataset=pd.read_csv(path,na_values='?',sep=" ",names=['class','a1','a2','a3','a4','a5','a6','Id'])
#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)

	dataset2 = pd.read_csv(path_test,na_values='?',sep=" ",names=['class','a1','a2','a3','a4','a5','a6','Id'])

	dataset = dataset.drop("Id",axis=1)
	dataset2 = dataset2.drop("Id",axis=1)

	dataset = dataset.reset_index(drop=True)
	dataset2 = dataset2.reset_index(drop=True)


	train_val_test(data = dataset, data2 = dataset2, list_classes = ["0", "1"],
				folder_name = "dataset_benchmark/monk2/", categorical_features =  [att for att in list(dataset) if att!='class'],
				numerical_features = [],
				dataset_name = "monk2", use_classes = False)

def read_monk3(path="dataset_benchmark/monk3/monks-3.train",path_test="dataset_benchmark/monk3/monks-3.test"):
	dataset=pd.read_csv(path,na_values='?',sep=" ",names=['class','a1','a2','a3','a4','a5','a6','Id'])
#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)

	dataset2 = pd.read_csv(path_test,na_values='?',sep=" ",names=['class','a1','a2','a3','a4','a5','a6','Id'])

	dataset = dataset.drop("Id",axis=1)
	dataset2 = dataset2.drop("Id",axis=1)

	dataset = dataset.reset_index(drop=True)
	dataset2 = dataset2.reset_index(drop=True)


	train_val_test(data = dataset, data2 = dataset2, list_classes = ["0", "1"],
				folder_name = "dataset_benchmark/monk3/", categorical_features =  [att for att in list(dataset) if att!='class'],
				numerical_features = [],
				dataset_name = "monk3", use_classes = False)


def read_seismic(path="dataset_benchmark/seismic/seismic_bumps.csv", path_test=None):
	dataset = pd.read_csv(path, delimiter=';')
	dataset = dataset.rename(columns ={"Target": "class"})

	mutiva_att=["Feat0", "Feat1", "Feat2", "Feat12", "Feat13", "Feat14", "Feat15"]
	num_att = [a for a in list(dataset) if a not in mutiva_att and a!="class"]

	train_val_test(data = dataset, list_classes = [str(i) for i in np.unique(dataset['class'].values)],
				folder_name = "dataset_benchmark/seismic/", numerical_features = num_att,
				categorical_features = mutiva_att,
				dataset_name = "seismic", use_classes = False)



def read_spambase(path="dataset_benchmark/spambase/spambase.csv", path_test=None):
	dataset=pd.read_csv(path,delimiter=';')
	#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)

	dataset = dataset.rename(columns ={"target": "class"})
	mutiva_att=[at for at in list(dataset) if at != "class"]

	train_val_test(data = dataset, list_classes = [str(i) for i in np.unique(dataset['class'].values)],
				folder_name = "dataset_benchmark/spambase/", numerical_features = mutiva_att,
				categorical_features = [],
				dataset_name = "spambase", use_classes = False)

def read_bank_marketing(path="dataset_benchmark/bank_marketing/bank-additional.csv", path_test=None):
	dataset=pd.read_csv(path,na_values='?',sep=";")
	#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)
	dataset=dataset.dropna()
	dataset=dataset.drop('duration',axis=1)
	dataset = dataset.rename(columns ={"y": "class"})

	mutiva_att=["age","campaign","pdays","previous","emp.var.rate","cons.price.idx","cons.conf.idx","euribor3m","nr.employed"]

	train_val_test(data = dataset, list_classes = [str(i) for i in np.unique(dataset['class'].values)],
				folder_name = "dataset_benchmark/bank_marketing/", numerical_features = mutiva_att,
				categorical_features = [att for att in list(dataset) if att not in mutiva_att and att!="class"],
				dataset_name = "bank_marketing", use_classes = False)

def read_pima_indian_diabetes(path="dataset_benchmark/pima_indian_diabetes/diabetes.csv", path_test=None):
	dataset=pd.read_csv(path,na_values='?')
#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)
#dataset=dataset.fillna(method = "bfill")
	dataset=dataset.dropna()
	dataset = dataset.rename(columns ={"Outcome": "class"})

	num_att=[at for at in list(dataset) if at != "class"]


	train_val_test(data = dataset, list_classes = ['No_Diabete',"Diabete"],
				folder_name = "dataset_benchmark/pima_indian_diabetes/", numerical_features = num_att,
				categorical_features = [],
				dataset_name = "pima_indian_diabetes", use_classes = False)

def read_ionosphere(path="dataset_benchmark/ionosphere/Ionosphere.csv", path_test=None):
	dataset=pd.read_csv(path,delimiter=';')
	#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)
	dataset=dataset.dropna()

	dataset = dataset.rename(columns ={"target": "class"})
	mutiva_att=[at for at in list(dataset) if at != "class"]

	train_val_test(data = dataset, list_classes = [str(i) for i in np.unique(dataset['class'].values)],
				folder_name = "dataset_benchmark/ionosphere/", numerical_features = mutiva_att,
				categorical_features = [],
				dataset_name = "ionosphere", use_classes = False)


def read_bank_note_authentication(path="dataset_benchmark/banknote_authentication/data_banknote_authentication.txt",
	path_test=None):
	dataset=pd.read_csv(path,na_values='?',
            names=['Variance_of_wavelet',"skewness_of_wavelet","curtosis_of_wavelet","entropy_of_image","class"])
	#X =np.asarray(dataset.values[:,0:dataset.shape[1]]-1,dtype=np.str)
	dataset=dataset.dropna()

	numeric_real=['Variance_of_wavelet',"skewness_of_wavelet","curtosis_of_wavelet","entropy_of_image"]

	train_val_test(data = dataset, list_classes = [str(i) for i in np.unique(dataset['class'].values)],
				folder_name = "dataset_benchmark/banknote_authentication/", numerical_features = numeric_real,
				categorical_features = [],
				dataset_name = "banknote_authentication", use_classes = False)