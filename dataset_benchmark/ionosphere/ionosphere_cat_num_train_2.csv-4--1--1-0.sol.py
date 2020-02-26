import csv
import sys
import os

train = "ionosphere_cat_num_train_2.csv"
test = "ionosphere_cat_num_test_2.csv"
def predict(row,header):
  if float(row[header["Feat26"]]) <= 0.9999450147151947:
    if float(row[header["Feat33"]]) <= 0.89895:
      if float(row[header["Feat6"]]) <= 0.883405:
        if float(row[header["Feat4"]]) <= 0.041440000000000005:
          return 0.0
        if float(row[header["Feat4"]]) > 0.041440000000000005:
          return 1.0
      if float(row[header["Feat6"]]) > 0.883405:
        if float(row[header["Feat2"]]) <= 0.736665:
          return 0.0
        if float(row[header["Feat2"]]) > 0.736665:
          return 1.0
    if float(row[header["Feat33"]]) > 0.89895:
      if float(row[header["Feat2"]]) <= 0.84748:
        if float(row[header["Feat22"]]) <= 0.020715:
          return 0.0
        if float(row[header["Feat22"]]) > 0.020715:
          return 1.0
      if float(row[header["Feat2"]]) > 0.84748:
        if float(row[header["Feat8"]]) <= 0.6750149999999999:
          return 0.0
        if float(row[header["Feat8"]]) > 0.6750149999999999:
          return 1.0
  if float(row[header["Feat26"]]) > 0.9999450147151947:
    if float(row[header["Feat20"]]) <= 0.969295:
      if float(row[header["Feat15"]]) <= 0.00143:
        if float(row[header["Feat0"]]) <= 0.5:
          return 0.0
        if float(row[header["Feat0"]]) > 0.5:
          return 0.0
      if float(row[header["Feat15"]]) > 0.00143:
        if float(row[header["Feat6"]]) <= 0.628035:
          return 0.0
        if float(row[header["Feat6"]]) > 0.628035:
          return 1.0
    if float(row[header["Feat20"]]) > 0.969295:
      if float(row[header["Feat15"]]) <= -0.22318:
        if float(row[header["Feat0"]]) <= 0.5:
          return 0.0
        if float(row[header["Feat0"]]) > 0.5:
          return 0.0
      if float(row[header["Feat15"]]) > -0.22318:
        if float(row[header["Feat15"]]) <= -0.053355:
          return 1.0
        if float(row[header["Feat15"]]) > -0.053355:
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
