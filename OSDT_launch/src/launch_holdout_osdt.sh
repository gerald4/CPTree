#!/bin/bash

#"""
#Created on Wed Feb 12 08:42:54 2020

#@author: gnanfack
#"""

for (( iter=$1; iter<=$2; iter++))
do
    for data in banknote_authentication biodeg credit_approval hepatitis mammographic_masses monk1 monk2 monk3 pima_indian_diabetes ionosphere seismic spambase spect_heart thoracy_surgery tic_tac_toe;
    do
    for (( depth=2; depth<=$3; depth++))
    do
	     if  (( $iter <= 1 )) ;
	    then
		    echo "$iter $data"
         python3 get_lambda.py $data $iter $depth
		   l=$(<"temp")
		   echo $l;
         python3 cross_val_testaccuracy.py --dataset_name=$data --lamb=$l --K=$depth --max_time=$4 --iter=$iter;
         else
	          if  [ "$data" != "monk1" ] && [ "$data" != "monk2" ] && [ "$data" != "monk3" ] && [ "$data" != "spect_heart" ] ;
	          then
		          	    echo "$iter $data"
		         python3 get_lambda.py $data $iter $depth
		   l=$(<"temp")
		   echo $l;
         python3 cross_val_testaccuracy.py --dataset_name=$data --lamb=$l --K=$depth --max_time=$4 --iter=$iter;
	          fi
         fi
    done
    done
done

echo "Finished"
