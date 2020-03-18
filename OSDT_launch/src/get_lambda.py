#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 08:36:37 2020

@author: gnanfack
"""

import sys


import pandas as pd

def main(argv):
	evaluation_method = "cat_dis_crossval"
	dataset = argv[1]
	step = argv[2]
	depth = argv[3]

	data = pd.read_csv(f'crossval_result/OSDT_{dataset}_{evaluation_method}_step={step}_depth={depth}.csv')


	with open("temp","w") as f:
		f.write(str(data.loc[data['osdt_test'].idxmax()]['lambda']))


if __name__ == '__main__':
	main(sys.argv[:])

