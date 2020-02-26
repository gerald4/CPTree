import csv
import sys
import os

train = "banknote_authentication_cat_num_train_3.csv"
test = "banknote_authentication_cat_num_test_3.csv"
def predict(row,header):
  if float(row[header["Variance_of_wavelet"]]) <= -0.279075:
    if float(row[header["skewness_of_wavelet"]]) <= 3.63155:
      if float(row[header["curtosis_of_wavelet"]]) <= 6.745599985122681:
        if float(row[header["skewness_of_wavelet"]]) <= 3.51985:
          return 1.0
        if float(row[header["skewness_of_wavelet"]]) > 3.51985:
          return 1.0
      if float(row[header["curtosis_of_wavelet"]]) > 6.745599985122681:
        if float(row[header["skewness_of_wavelet"]]) <= 1.2797999999999998:
          return 1.0
        if float(row[header["skewness_of_wavelet"]]) > 1.2797999999999998:
          return 0.0
    if float(row[header["skewness_of_wavelet"]]) > 3.63155:
      if float(row[header["skewness_of_wavelet"]]) <= 9.28895:
        if float(row[header["Variance_of_wavelet"]]) <= -1.95915:
          return 1.0
        if float(row[header["Variance_of_wavelet"]]) > -1.95915:
          return 0.0
      if float(row[header["skewness_of_wavelet"]]) > 9.28895:
        if float(row[header["skewness_of_wavelet"]]) <= 9.30865:
          return 1.0
        if float(row[header["skewness_of_wavelet"]]) > 9.30865:
          return 0.0
  if float(row[header["Variance_of_wavelet"]]) > -0.279075:
    if float(row[header["entropy_of_image"]]) <= -0.0584185:
      if float(row[header["skewness_of_wavelet"]]) <= 5.21045:
        if float(row[header["curtosis_of_wavelet"]]) <= 0.193355:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > 0.193355:
          return 0.0
      if float(row[header["skewness_of_wavelet"]]) > 5.21045:
        if float(row[header["skewness_of_wavelet"]]) <= 2.25655:
          return 1.0
        if float(row[header["skewness_of_wavelet"]]) > 2.25655:
          return 0.0
    if float(row[header["entropy_of_image"]]) > -0.0584185:
      if float(row[header["Variance_of_wavelet"]]) <= 0.7581600000000001:
        if float(row[header["curtosis_of_wavelet"]]) <= 2.13455:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > 2.13455:
          return 0.0
      if float(row[header["Variance_of_wavelet"]]) > 0.7581600000000001:
        if float(row[header["curtosis_of_wavelet"]]) <= -1.6317:
          return 1.0
        if float(row[header["curtosis_of_wavelet"]]) > -1.6317:
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
