import csv
import sys
import os

train = "wine_cat_num_train_1.csv"
test = "wine_cat_num_test_1.csv"
def predict(row,header):
  if float(row[header["Feat4"]]) <= 119.5:
    if float(row[header["Feat6"]]) <= 1.4:
      if float(row[header["Feat9"]]) <= 3.8449999999999998:
        return 1.0
      if float(row[header["Feat9"]]) > 3.8449999999999998:
        return 2.0
    if float(row[header["Feat6"]]) > 1.4:
      if float(row[header["Feat12"]]) <= 719.0:
        return 1.0
      if float(row[header["Feat12"]]) > 719.0:
        return 0.0
  if float(row[header["Feat4"]]) > 119.5:
    if float(row[header["Feat10"]]) <= 1.2349999999999999:
      if float(row[header["Feat6"]]) <= 2.1799999999999997:
        return 2.0
      if float(row[header["Feat6"]]) > 2.1799999999999997:
        return 0.0
    if float(row[header["Feat10"]]) > 1.2349999999999999:
      if float(row[header["Feat0"]]) <= 13.629999999999999:
        return 1.0
      if float(row[header["Feat0"]]) > 13.629999999999999:
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
