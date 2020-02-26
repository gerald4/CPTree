import csv
import sys
import os

train = "ionosphere_cat_num_train_3.csv"
test = "ionosphere_cat_num_test_3.csv"
def predict(row,header):
  if float(row[header["Feat4"]]) <= 0.14597500000000002:
    if float(row[header["Feat4"]]) <= 0.041440000000000005:
      if float(row[header["Feat33"]]) <= 0.020624999999999998:
        return 0.0
      if float(row[header["Feat33"]]) > 0.020624999999999998:
        return 0.0
    if float(row[header["Feat4"]]) > 0.041440000000000005:
      if float(row[header["Feat11"]]) <= -0.01134:
        return 0.0
      if float(row[header["Feat11"]]) > -0.01134:
        return 1.0
  if float(row[header["Feat4"]]) > 0.14597500000000002:
    if float(row[header["Feat7"]]) <= -0.48282:
      if float(row[header["Feat21"]]) <= -0.8430200000000001:
        return 1.0
      if float(row[header["Feat21"]]) > -0.8430200000000001:
        return 0.0
    if float(row[header["Feat7"]]) > -0.48282:
      if float(row[header["Feat26"]]) <= 0.999210000038147:
        return 1.0
      if float(row[header["Feat26"]]) > 0.999210000038147:
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
