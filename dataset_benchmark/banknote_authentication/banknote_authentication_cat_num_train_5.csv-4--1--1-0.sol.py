import csv
import sys
import os

train = "banknote_authentication_cat_num_train_5.csv"
test = "banknote_authentication_cat_num_test_5.csv"
def predict(row,header):
  if float(row[header["Variance_of_wavelet"]]) <= 0.33218000000000003:
    if float(row[header["skewness_of_wavelet"]]) <= 6.9910499999999995:
      if float(row[header["skewness_of_wavelet"]]) <= 4.10545:
        if float(row[header["Variance_of_wavelet"]]) <= 0.32016500000000003:
          return 1.0
        if float(row[header["Variance_of_wavelet"]]) > 0.32016500000000003:
          return 0.0
      if float(row[header["skewness_of_wavelet"]]) > 4.10545:
        if float(row[header["entropy_of_image"]]) <= -1.43555:
          return 1.0
        if float(row[header["entropy_of_image"]]) > -1.43555:
          return 0.0
    if float(row[header["skewness_of_wavelet"]]) > 6.9910499999999995:
      if float(row[header["entropy_of_image"]]) <= -2.5612000000000004:
        if float(row[header["Variance_of_wavelet"]]) <= -2.7515:
          return 1.0
        if float(row[header["Variance_of_wavelet"]]) > -2.7515:
          return 0.0
      if float(row[header["entropy_of_image"]]) > -2.5612000000000004:
        if float(row[header["skewness_of_wavelet"]]) <= -2.06515:
          return 0.0
        if float(row[header["skewness_of_wavelet"]]) > -2.06515:
          return 0.0
  if float(row[header["Variance_of_wavelet"]]) > 0.33218000000000003:
    if float(row[header["skewness_of_wavelet"]]) <= 2.9114500000000003:
      if float(row[header["Variance_of_wavelet"]]) <= 3.304050087928772:
        if float(row[header["curtosis_of_wavelet"]]) <= 0.573795:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > 0.573795:
          return 0.0
      if float(row[header["Variance_of_wavelet"]]) > 3.304050087928772:
        if float(row[header["Variance_of_wavelet"]]) <= -0.11181999999999999:
          return 0.0
        if float(row[header["Variance_of_wavelet"]]) > -0.11181999999999999:
          return 0.0
    if float(row[header["skewness_of_wavelet"]]) > 2.9114500000000003:
      if float(row[header["Variance_of_wavelet"]]) <= 2.22845:
        if float(row[header["curtosis_of_wavelet"]]) <= -3.05495:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > -3.05495:
          return 0.0
      if float(row[header["Variance_of_wavelet"]]) > 2.22845:
        if float(row[header["entropy_of_image"]]) <= -3.231:
          return 0.0
        if float(row[header["entropy_of_image"]]) > -3.231:
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
