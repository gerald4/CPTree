#!/bin/bash

#"""
#Created on Wed Jan 29 15:32:41 2020
#@author: gnanfack
#"""


for (( iter=$1; iter<=$2; iter++))
do
    for data in banknote_authentication biodeg credit_approval hepatitis ionosphere mammographic_masses monk1 monk2 monk3 pima_indian_diabetes ionosphere seismic spambase spect_heart thoracy_surgery tic_tac_toe;
    do
    for (( depth=2; depth<=$3; depth++))
    do
        python3 test_accuracy.py --dataset_name=$data --K=$depth --max_time=$4 --iter=$iter;
    done
    done
done

echo "Finished"
