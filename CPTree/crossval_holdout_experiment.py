#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 09:59:33 2020

@author: gnanfack
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas as pd
import os


import numpy as np

from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
from sklearn import tree as cart_tree
from sklearn.preprocessing import LabelBinarizer
import argparse

plt.style.use('classic')

from utils import decisionTreeConstraint, predict, export_graphviz_cp


if __name__=='__main__':

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


	v=2

	path_train = '../dataset_benchmark/'+dataset+'/'+dataset+'_cat_dis_holdout_train_'+str(step)+'.csv'
	path_test = '../dataset_benchmark/'+dataset+'/'+dataset+'_cat_dis_holdout_test_'+str(step)+'.csv'

	data_train = pd.DataFrame(pd.read_csv(path_train, sep=";"))
	data_test = pd.DataFrame(pd.read_csv(path_test, sep=";"))

	X_train = data_train.values[:, :-1]
	y_train = data_train.values[:, -1]

	X_test = data_test.values[:, :-1]
	y_test = data_test.values[:, -1]

	C=np.unique(y_train)
	lb=LabelBinarizer()
	lb.fit(C)
	y_train_ohot=lb.transform(y_train)
	y_test_ohot=lb.transform(y_test)
	if len(C)==2:
		y_train_ohot= np.hstack((1-y_train_ohot, y_train_ohot))
		y_test_ohot= np.hstack((1-y_test_ohot, y_test_ohot))

	N = X_train.shape[0]
	M = X_train.shape[1]
	class_names = [str(i) for i in C]
	col_names = list(data_train)[:-1]
	C=class_names
	filepath='../dataset_benchmark/'+dataset+'/CPtree_bis_crossval_result_'+dataset+'.csv'


	print("*******Model Construction********")
	print("******Iteration ", str(step))
	print("******Dataset ", dataset)

	tree, optimal, ttime =decisionTreeConstraint(L= l, K= k, V=v, max_time=max_time, X=X_train, Y=y_train_ohot,
                             colnames=col_names,
                        classnames=class_names,imbalanced=False, C = C)
	if tree:
		tree1=export_graphviz_cp(tree)
		y_pre_test=[predict(tree,X_test[i,:]) for i in range(X_test.shape[0])]
		y_pre_train=[predict(tree,X_train[i,:]) for i in range(X_train.shape[0])]
		test_accuracy=accuracy_score(y_pre_test,np.argmax(y_test_ohot,axis=1))
		train_accuracy=accuracy_score(y_pre_train,np.argmax(y_train_ohot,axis=1))
		clf=cart_tree.DecisionTreeClassifier(criterion='entropy',max_leaf_nodes=l,max_depth=k)
		clf.fit(X_train,y_train)


		cart_train_accuracy=accuracy_score(y_train,clf.predict(X_train))
		cart_test_accuracy=accuracy_score(y_test,clf.predict(X_test))
		#		try:
#			tree1.render(name1)
#		except:
#			pass
#		try:
#			graph.render(name2)
#		except:
#			pass

		mode = 'a' if os.path.exists(filepath) else 'w'
		with open(filepath, mode) as f:
			if f.tell()==0:
				f.write("dataset_name,step,optimality, time_taken,L,K,cart_train,cp_tree_train,cart_test,cp_tree_test\n"+dataset+","+str(step)+","+optimal+","+str(ttime/60)+","+str(l)+","+str(k)+","+str(cart_train_accuracy)+","+str(train_accuracy)+","+str(cart_test_accuracy)+","+str(test_accuracy)+"\n")
			else:
				f.write(dataset+","+str(step)+","+optimal+","+str(ttime/60)+","+str(l)+","+str(k)+","+str(cart_train_accuracy)+","+str(train_accuracy)+","+str(cart_test_accuracy)+","+str(test_accuracy)+"\n")
		print("dataset: ",dataset,"step: ",str(step), "optimality: ", optimal, "CP-Tree: ", "Leaves: ",l, ", Depth: ",k, ", test accuracy: ", test_accuracy,", train accuracy: ", train_accuracy)
		print("dataset: ", dataset,"step: ",str(step), "optimality: ", optimal,"CART: ", "Leaves: ",l, ", Depth: ",k, ", test accuracy: ", cart_test_accuracy,", train accuracy: ", cart_train_accuracy)

	else:
#		with open(filename+dataset_name+"cart_cptree_final.csv", 'a') as f:
#			if f.tell()==0:
#				f.write("step,L,K,cart_train,cp_tree_train,cart_test,cp_tree_test\n"+str(step)+","+str(l)+","+str(k)+","+str(-1)+","+str(-1)+","+str(-1)+","+str(-1)+"\n")
#			else:
#				f.write(str(step)+","+str(l)+","+str(k)+","+str(-1)+","+str(-1)+","+str(-1)+","+str(-1)+"\n")
		print("dataset: ", dataset,"CP-Tree: ", "Leaves: ",l, ", Depth: ",k, ", test accuracy: ", -1,", train accuracy: ", -1)
