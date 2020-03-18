import pandas as pd
import numpy as np
import heapq
import math
import time
import os

import gmpy2
from gmpy2 import mpz
import re

from sklearn import tree

import cProfile

from random import randint, sample, seed

import matplotlib.pyplot as plt

from sklearn.model_selection import KFold # import KFold

from osdt import bbound, predict

import argparse

# Read in the dataset

#compas = pd.DataFrame(pd.read_csv('../../data/dataset_benchmark/compas-binary.csv',sep=";"))
# =============================================================================
# seismic = pd.DataFrame(pd.read_csv('../../dataset_benchmark/{seismic}/{seismic}_cat_dis_holdout_train_1.csv',sep=";"))
# monk1 = pd.DataFrame(pd.read_csv('../../dataset_benchmark/{monk1}/{monk1}_cat_dis_holdout_train_1.csv',sep=";"))
# monk2 = pd.DataFrame(pd.read_csv('../../dataset_benchmark/{seismic}/{seismic}_cat_dis_holdout_train_1.csv',sep=";"))
# monk3 = pd.DataFrame(pd.read_csv('../data/preprocessed/monk3-train.csv',sep=";"))
# balance = pd.DataFrame(pd.read_csv('../data/preprocessed/balance-scale.csv',sep=";"))
# tictactoe = pd.DataFrame(pd.read_csv('../data/preprocessed/tic-tac-toe.csv',sep=";"))
# car = pd.DataFrame(pd.read_csv('../data/preprocessed/car-evaluation.csv',sep=";"))
#
# =============================================================================




def test_accuracy(dataset, step, lambs, timelimit=600, depth = 3):
	"""
    Run CART and OSDT
    split data into 3 folds, with 2 folds to train, 1 fold to test
    :param X:
    :param y:
    :param lambs:
    :param file_CART:
    :param file_OSDT:
    :return:
	"""
#    with open(file_CART, 'a+') as f:
#        f.write(";".join(["depth", "lamb", "nleaves", "trainaccu_CART", "testaccu_CART"]) + '\n')
# =============================================================================
#     with open(file_OSDT, 'a+') as f:
#         f.write(";".join(["depth", "lamb", "nleaves", "trainaccu_OSDT", "testaccu_OSDT", "totaltime", "time_c", "leaves_c"]) + '\n')
# =============================================================================
	file_train = f'../../dataset_benchmark/{dataset}/{dataset}_{evaluation_method}_train_{step}.csv'
	filepath = f'crossval_result/OSDT_{dataset}_{evaluation_method}_step={step}_depth={depth}.csv'
	for lamb in lambs:
        #for i in range(1, 11): # 10 folds

		file_test = file_train.replace("train","val")

		data_train = pd.DataFrame(pd.read_csv(file_train, sep=";"))
		data_test = pd.DataFrame(pd.read_csv(file_test, sep=";"))

		X_train = data_train.values[:, :-1]
		y_train = data_train.values[:, -1]

		X_test = data_test.values[:, :-1]
		y_test = data_test.values[:, -1]

            # CART
# =============================================================================
#         for depth in range(2,5):
#
#             clf = tree.DecisionTreeClassifier(max_depth=depth, min_samples_split=max(math.ceil(lamb * 2 * len(y_train)), 2),
#                                               min_samples_leaf=math.ceil(lamb * len(y_train)),
#                                               max_leaf_nodes=math.floor(1 / (2 * lamb)),
#                                               min_impurity_decrease=lamb
#                                               )
#
#             clf = clf.fit(X_train, y_train)
#
#             nleaves_CART = (clf.tree_.node_count + 1) / 2
#             trainaccu_CART = clf.score(X_train, y_train)
#             testaccu_CART = clf.score(X_test, y_test)
# =============================================================================

            #yhat0 = clf.predict(X_test)

            #print("yhat0!!!", yhat0)
            #print("y!!!", y_test)

            #print("<<<<<<<<<<<<<<<<< clf0:", clf)

            #print(">>>>>>>>>>>>>>>>> testaccu_CART:", testaccu_CART)


            # OSDT
		leaves_c, prediction_c, dic, nleaves_OSDT, nrule, ndata, totaltime, time_c, COUNT, C_c, trainaccu_OSDT, best_is_cart, clf =\
                    bbound(X_train, y_train, lamb=lamb, prior_metric="curiosity", timelimit=timelimit, init_cart=False, MAXDEPTH = depth)
		_, testaccu_OSDT = predict(leaves_c, prediction_c, dic, X_test, y_test, best_is_cart, clf)

# =============================================================================
# 		with open(file_OSDT, 'a+') as f:
# 			f.write(";".join(
#                         [str(depth), str(lamb), str(nleaves_OSDT), str(trainaccu_OSDT), str(testaccu_OSDT),
#                          str(totaltime), str(time_c), str(leaves_c)]) + '\n')
# =============================================================================

		mode = 'a' if os.path.exists(filepath) else 'w'
		with open(filepath, mode) as f:
			if f.tell()==0:
				f.write("dataset_name,step,lambda,time_taken,K,L,osdt_train,osdt_test\n"+dataset+","+str(step)+","+str(lamb)+","+str(totaltime/60)+","+str(depth)+","+str(nleaves_OSDT)+","+str(trainaccu_OSDT)+","+str(testaccu_OSDT)+"\n")
			else:
				f.write(dataset+","+str(step)+","+str(lamb)+","+str( totaltime/60)+","+str(depth)+","+str(nleaves_OSDT)+","+str(trainaccu_OSDT)+","+str(testaccu_OSDT)+"\n")
#"""

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parameters')

	parser.add_argument('--dataset_name', help="the name of the dataset", default="car")

	parser.add_argument('--K', help="maximum depth", type=int, default=3)
	parser.add_argument("--max_time",help="maximum time", type=int, default=600)
	parser.add_argument("--iter",help="iteration", type=int, default=0)


	args = parser.parse_args()



	k=args.K
	max_time=args.max_time
	dataset=args.dataset_name
	step=args.iter
	lambs1 = [0.1, 0.05, 0.01, 0.005, 0.0025]

	evaluation_method = "cat_dis_crossval"

	test_accuracy(dataset = dataset, step = step, lambs = lambs1, timelimit= max_time, depth = k)


# =============================================================================
# dataname = ["banknote_authentication", "biodeg", "credit_approval", "hepatitis",
#  		   "ionosphere", "mammographic_masses", "monk1", "monk2", "monk3", "pima_indian_diabetes",
#  		    "seismic", "spambase", "spect_heart", "thoracy_surgery", "tic_tac_toe"
# 			 ]
# =============================================================================


# =============================================================================
# for dataset in dataname:
# 	test_accuracy(dataset = dataset, step = 1, lambs = lambs1, timelimit= max_time, depth = 4)
# =============================================================================
# =============================================================================
# dataname="seismic"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs=lambs1,
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')
#
# dataname="car"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs=lambs1, #lambs,
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')
#
# dataname="tic_tac_toe"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs=lambs1,
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')
# =============================================================================
# dataname="balance_scale"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs = lambs1, #lambs=[0.05, 0.005, 0.001, 0.00035],
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')

# dataname="monk1"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs=[0.1, 0.05, 0.025],
#                file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')

# dataname="monk2"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs = lambs1,#=[0.1, 0.025, 0.01, 0.005],
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')

# dataname="monk3"
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs = lambs1, #lambs=[0.1, 0.025, 0.01, 0.005],
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')


# =============================================================================
# test_accuracy(f'../../dataset_benchmark/{dataname}/{dataname}_cat_dis_holdout_train_1.csv', lambs = lambs1, #lambs=[0.1, 0.025, 0.01, 0.005],
#               file_CART=f'./accuracy/cart_{dataname}_1.txt', file_OSDT=f'./accuracy/osdt_{dataname}_1.txt')
# =============================================================================


#"""

# =============================================================================
# def test_accuracy_onefold(file, lambs, file_CART, file_OSDT, timelimit):
#     """
#     Run CART and OSDT
#     use all data, only training accuracy
#     :param X:
#     :param y:
#     :param lambs:
#     :param file_CART:
#     :param file_OSDT:
#     :return:
#     """
#     with open(file_CART, 'a+') as f:
#         f.write(";".join(["depth", "lamb", "nleaves", "trainaccu_CART", "testaccu_CART"]) + '\n')
#     with open(file_OSDT, 'a+') as f:
#         f.write(";".join(["fold", "lamb", "nleaves", "trainaccu_OSDT", "testaccu_OSDT", "totaltime", "time_c", "leaves_c"]) + '\n')
#     for lamb in lambs:
#
#         file_train = file
#
#         data_train = pd.DataFrame(pd.read_csv(file_train, sep=";"))
#
#         X_train = data_train.values[:, :-1]
#         y_train = data_train.values[:, -1]
#
#
#         # CART
#         for depth in range(2,5):
#             clf = tree.DecisionTreeClassifier(max_depth=depth, min_samples_split=max(math.ceil(lamb * 2 * len(y_train)), 2),
#                                           min_samples_leaf=math.ceil(lamb * len(y_train)),
#                                           max_leaf_nodes=math.floor(1 / (2 * lamb)),
#                                           min_impurity_decrease=lamb
#                                           )
#             clf = clf.fit(X_train, y_train)
#
#             nleaves_CART = (clf.tree_.node_count + 1) / 2
#             trainaccu_CART = clf.score(X_train, y_train)
#
#             with open(file_CART, 'a+') as f:
#                 f.write(";".join([str('NA'), str(lamb), str(nleaves_CART), str(trainaccu_CART), str('NA')]) + '\n')
#
#         # OSDT
#                 leaves_c, prediction_c, dic, nleaves_OSDT, nrule, ndata, totaltime, time_c, COUNT, C_c, trainaccu_OSDT, best_is_cart, clf =\
#                 bbound(X_train, y_train, lamb=lamb, prior_metric="curiosity", timelimit=timelimit, init_cart=True, MAXDEPTH = depth)
#
#             with open(file_OSDT, 'a+') as f:
#                 f.write(";".join(
#                     [str('NA'), str(lamb), str(nleaves_OSDT), str(trainaccu_OSDT), str('NA'),
#                  str(totaltime), str(time_c), str(leaves_c)]) + '\n')
# =============================================================================

# =============================================================================
#             if nleaves_OSDT >= 16:
#                 break
#
# =============================================================================


# =============================================================================
# lambs1 = [0.1, 0.05, 0.01, 0.005, 0.0025]
#
# timelimi1 = 1800
# #timelimi2 = 7200 # set time limit to be 2h
# #'''
# test_accuracy_onefold('../data/preprocessed/compas-binary.csv', lambs=[0.025, 0.01, 0.005, 0.001, 0.0005],
#                       file_CART=r'./accuracy/cart_compas.txt', file_OSDT=r'./accuracy/osdt_compas.txt', timelimit=timelimi1)
#
#
# test_accuracy_onefold('../data/preprocessed/car-evaluation.csv', lambs=lambs1,
#                       file_CART=r'./accuracy/cart_car.txt', file_OSDT=r'./accuracy/osdt_car.txt', timelimit=timelimi1)
#
#
# test_accuracy_onefold('../data/preprocessed/tic-tac-toe.csv', lambs=lambs1,
#                       file_CART=r'./accuracy/cart_tictactoe.txt', file_OSDT=r'./accuracy/osdt_tictactoe.txt', timelimit=timelimi1)
#
# test_accuracy_onefold('../data/preprocessed/fico_binary.csv', lambs=[0.05, 0.005, 0.001, 0.00035],
#                       file_CART=r'./accuracy/cart_fico.txt', file_OSDT=r'./accuracy/osdt_fico.txt', timelimit=timelimi1)
#
# test_accuracy_onefold('../data/preprocessed/monk1-train.csv', lambs=[0.1, 0.05, 0.025],
#                       file_CART=r'./accuracy/cart_monk1.txt', file_OSDT=r'./accuracy/osdt_monk1.txt', timelimit=timelimi1)
#
# test_accuracy_onefold('../data/preprocessed/monk2-train.csv', lambs=[0.1, 0.025, 0.01, 0.005],
#                       file_CART=r'./accuracy/cart_monk2.txt', file_OSDT=r'./accuracy/osdt_monk2.txt', timelimit=timelimi1)
#
#
# test_accuracy_onefold('../data/preprocessed/monk3-train.csv', lambs=[0.1, 0.025, 0.01, 0.005],
#                       file_CART=r'./accuracy/cart_monk3.txt', file_OSDT=r'./accuracy/osdt_monk3.txt', timelimit=timelimi1)
# =============================================================================
#'''