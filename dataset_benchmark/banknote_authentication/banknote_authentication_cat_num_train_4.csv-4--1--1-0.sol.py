import csv
import sys
import os

train = "banknote_authentication_cat_num_train_4.csv"
test = "banknote_authentication_cat_num_test_4.csv"
def predict(row,header):
  if float(row[header["skewness_of_wavelet"]]) <= 5.21045:
    if float(row[header["Variance_of_wavelet"]]) <= 0.31155499815940857:
      if float(row[header["skewness_of_wavelet"]]) <= -2.4149000000000003:
        if float(row[header["skewness_of_wavelet"]]) <= -1.60475:
          return 1.0
        if float(row[header["skewness_of_wavelet"]]) > -1.60475:
          return 1.0
      if float(row[header["skewness_of_wavelet"]]) > -2.4149000000000003:
        if float(row[header["curtosis_of_wavelet"]]) <= 4.8207:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > 4.8207:
          return 0.0
    if float(row[header["Variance_of_wavelet"]]) > 0.31155499815940857:
      if float(row[header["Variance_of_wavelet"]]) <= 2.3921:
        if float(row[header["curtosis_of_wavelet"]]) <= 0.222485:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > 0.222485:
          return 0.0
      if float(row[header["Variance_of_wavelet"]]) > 2.3921:
        if float(row[header["entropy_of_image"]]) <= -1.3315000000000001:
          return 0.0
        if float(row[header["entropy_of_image"]]) > -1.3315000000000001:
          return 0.0
  if float(row[header["skewness_of_wavelet"]]) > 5.21045:
    if float(row[header["entropy_of_image"]]) <= -1.6734499999999999:
      if float(row[header["curtosis_of_wavelet"]]) <= 6.5224:
        if float(row[header["Variance_of_wavelet"]]) <= -2.7952:
          return 1.0
        if float(row[header["Variance_of_wavelet"]]) > -2.7952:
          return 0.0
      if float(row[header["curtosis_of_wavelet"]]) > 6.5224:
        if float(row[header["skewness_of_wavelet"]]) <= -0.72322:
          return 1.0
        if float(row[header["skewness_of_wavelet"]]) > -0.72322:
          return 0.0
    if float(row[header["entropy_of_image"]]) > -1.6734499999999999:
      if float(row[header["Variance_of_wavelet"]]) <= -0.36031500000000005:
        if float(row[header["Variance_of_wavelet"]]) <= 2.3921:
          return 0.0
        if float(row[header["Variance_of_wavelet"]]) > 2.3921:
          return 0.0
      if float(row[header["Variance_of_wavelet"]]) > -0.36031500000000005:
        if float(row[header["curtosis_of_wavelet"]]) <= 2.41515:
          return 0.0
        if float(row[header["curtosis_of_wavelet"]]) > 2.41515:
          return 0.0


def main(argv):
  header = 0
  num_correct = 0
  num_total = -1
  preds = dict()
  with open(argv[0], 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
      num_total = num_total + 1
      if header == 0:
        header = dict()
        for i in range(len(row)):
          header[row[i]] = i
      else:
        pred = predict(row,header)
        orig = row[len(row)-1]
        #print(row, pred, orig)
        if int(float(pred)) == int(float(orig)):
          num_correct = num_correct + 1
        if str(pred) + " - " + str(orig) not in preds:
          preds[str(pred) + " - " + str(orig)] = 0
        preds[str(pred) + " - " + str(orig)] = preds[str(pred) + " - " + str(orig)] + 1
  print("num_correct", num_correct)
  print("accuracy", float(num_correct) / float(num_total))
  print("crosstable", preds)
  f = open(os.path.basename(__file__)+"-"+argv[0] + ".result.txt","w")
  f.write("accuracy " + str(num_correct / float(num_total)))
  f.write("crosstable " + str(preds))

main([train])
main([test])
