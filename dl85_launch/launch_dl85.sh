#!/bin/bash

#Created on Fri Jan 17 12:45:06 2020

#@author: gnanfack
#"""




# for value in $(seq $2 $3)
for (( iter=$1; iter<=$2; iter++))
do
    for data in balance_scale banknote_authentication biodeg car credit_approval hepatitis ionosphere iris mammographic_masses monk1 monk2 monk3 pima_indian_diabetes post_operative_patient seismic spambase spect_heart thoracy_surgery tic_tac_toe wine;
#    for data in tic_tac_toe;
    do
    for (( depth=2; depth<=$3; depth++))
    do	
        python3 dl85_test.py --dataset_name=$data --L=$((2 ** depth)) --K=$depth --max_time=$4 --iter=$iter;
    done
    done
done

echo "Finished"
