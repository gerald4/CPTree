#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 23:33:40 2020

@author: labogeraldo

"""
import sys


import pandas as pd

def main(argv):
	evaluation_method = "cat_dis_crossval"
	dataset = argv[1]
	step = argv[2]
	depth = argv[3]

	data = pd.read_csv(f"crossval_result/CPTree_{dataset}_{evaluation_method}_step={step}_depth={depth}.csv")


	with open("temp","w") as f:
		df = data.sort_values(by = ['cp_tree_test', 'L'], ascending=[False,True])
		f.write(str(df.loc[df['cp_tree_test'].idxmax()]['L']))


if __name__ == '__main__':
	main(sys.argv[:])

