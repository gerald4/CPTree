import csv
import sys
import os

train = "wine_cat_num_train_3.csv"
test = "wine_cat_num_test_3.csv"
def predict(row,header):
  if float(row[header["Feat5"]]) <= 2.605:
    if float(row[header["Feat9"]]) <= 7.15:
      if float(row[header["Feat6"]]) <= 1.335:
        if float(row[header["Feat9"]]) <= 3.49:
          return 1.0
        if float(row[header["Feat9"]]) > 3.49:
          return 2.0
      if float(row[header["Feat6"]]) > 1.335:
        if float(row[header["Feat12"]]) <= 875.0:
          return 1.0
        if float(row[header["Feat12"]]) > 875.0:
          return 0.0
    if float(row[header["Feat9"]]) > 7.15:
      if float(row[header["Feat12"]]) <= 1000.0:
        if float(row[header["Feat0"]]) <= 14.175:
          return 2.0
        if float(row[header["Feat0"]]) > 14.175:
          return 2.0
      if float(row[header["Feat12"]]) > 1000.0:
        if float(row[header["Feat2"]]) <= 2.455:
          return 2.0
        if float(row[header["Feat2"]]) > 2.455:
          return 0.0
  if float(row[header["Feat5"]]) > 2.605:
    if float(row[header["Feat12"]]) <= 673.5:
      if float(row[header["Feat0"]]) <= 14.125:
        if float(row[header["Feat12"]]) <= 666.0:
          return 1.0
        if float(row[header["Feat12"]]) > 666.0:
          return 0.0
      if float(row[header["Feat0"]]) > 14.125:
        if float(row[header["Feat5"]]) <= 2.41:
          return 2.0
        if float(row[header["Feat5"]]) > 2.41:
          return 2.0
    if float(row[header["Feat12"]]) > 673.5:
      if float(row[header["Feat9"]]) <= 3.5749999284744263:
        if float(row[header["Feat5"]]) <= 2.9699999999999998:
          return 1.0
        if float(row[header["Feat5"]]) > 2.9699999999999998:
          return 1.0
      if float(row[header["Feat9"]]) > 3.5749999284744263:
        if float(row[header["Feat1"]]) <= 4.395:
          return 0.0
        if float(row[header["Feat1"]]) > 4.395:
          return 2.0


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
