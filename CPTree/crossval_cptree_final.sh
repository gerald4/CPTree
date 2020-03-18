#!/bin/bash
# -*- coding: utf-8 -*-
#"""
#Created on Sun Feb  2 14:37:01 2020
#@author: labogeraldo
#"""


for (( iter=$1; iter<=$2; iter++))
do
    for data in monk1 monk2 monk3 spect_heart; #balance_scale banknote_authentication biodeg car credit_approval hepatitis ionosphere iris mammographic_masses pima_indian_diabetes post_operative_patient seismic spambase thoracy_surgery tic_tac_toe wine;
    do
    for (( depth=2; depth<=$3; depth++))
    do
#	    if  (($data != "monk1")) && (($data != "monk2")) && (($data != "monk3")) && (($data != "spect_heart")) ;
#	    then
		   python3 get_leaves_cptree.py $data $iter $depth
		   l=$(<"temp")
		   echo $l;
	         python3 crossval_holdout_experiment.py --dataset_name=$data --L=$l --K=$depth --max_time=$4 --iter=$iter;
 #       fi
    done
    done
done

echo "Finished"
