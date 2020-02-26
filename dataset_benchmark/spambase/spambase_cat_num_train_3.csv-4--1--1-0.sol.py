import csv
import sys
import os

train = "spambase_cat_num_train_3.csv"
test = "spambase_cat_num_test_3.csv"
def predict(row,header):
  if float(row[header["Feat51"]]) <= 0.2175:
    if float(row[header["Feat52"]]) <= 0.04450000077486038:
      if float(row[header["Feat14"]]) <= 0.315:
        if float(row[header["Feat22"]]) <= 0.225:
          return 0.0
        if float(row[header["Feat22"]]) > 0.225:
          return 1.0
      if float(row[header["Feat14"]]) > 0.315:
        if float(row[header["Feat4"]]) <= 0.715:
          return 0.0
        if float(row[header["Feat4"]]) > 0.715:
          return 1.0
    if float(row[header["Feat52"]]) > 0.04450000077486038:
      if float(row[header["Feat31"]]) <= 0.475:
        if float(row[header["Feat38"]]) <= 0.665:
          return 1.0
        if float(row[header["Feat38"]]) > 0.665:
          return 1.0
      if float(row[header["Feat31"]]) > 0.475:
        if float(row[header["Feat31"]]) <= 0.475:
          return 1.0
        if float(row[header["Feat31"]]) > 0.475:
          return 0.0
  if float(row[header["Feat51"]]) > 0.2175:
    if float(row[header["Feat27"]]) <= 0.165:
      if float(row[header["Feat12"]]) <= 0.135:
        if float(row[header["Feat41"]]) <= 0.455:
          return 1.0
        if float(row[header["Feat41"]]) > 0.455:
          return 0.0
      if float(row[header["Feat12"]]) > 0.135:
        if float(row[header["Feat54"]]) <= 1.322:
          return 0.0
        if float(row[header["Feat54"]]) > 1.322:
          return 1.0
    if float(row[header["Feat27"]]) > 0.165:
      if float(row[header["Feat27"]]) <= 0.195:
        if float(row[header["Feat41"]]) <= 0.455:
          return 1.0
        if float(row[header["Feat41"]]) > 0.455:
          return 0.0
      if float(row[header["Feat27"]]) > 0.195:
        if float(row[header["Feat10"]]) <= 0.185:
          return 0.0
        if float(row[header["Feat10"]]) > 0.185:
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
