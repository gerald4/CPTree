#!/bin/bash
# -*- coding: utf-8 -*-
#"""
#Created on Sun Feb  2 14:37:01 2020
#@author: labogeraldo
#"""


for (( iter=$1; iter<=$2; iter++))
do
    for data in balance_scale banknote_authentication biodeg car credit_approval hepatitis ionosphere iris mammographic_masses monk1 monk2 monk3 pima_indian_diabetes post_operative_patient seismic spambase spect_heart thoracy_surgery tic_tac_toe wine;
    do
    for (( depth=3; depth<=$3; depth++))
    do

        #for ((l=$((3 *depth - 3)); l <= $((2 ** depth)); l++ ))
        for ((l=$((depth + 1)); l <= $((3*depth - 4)); l++ ))
	do
         python3 crossval_experiment.py --dataset_name=$data --L=$l --K=$depth --max_time=$4 --iter=$iter;
        done
    done
    done
done

echo "Finished"
