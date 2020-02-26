import csv
import sys
import os

train = "spambase_cat_num_train_5.csv"
test = "spambase_cat_num_test_5.csv"
def predict(row,header):
  if float(row[header["Feat24"]]) <= 0.7:
    if float(row[header["Feat23"]]) <= 10.795:
      if float(row[header["Feat51"]]) <= 0.0755:
        if float(row[header["Feat40"]]) <= 0.09:
          return 0.0
        if float(row[header["Feat40"]]) > 0.09:
          return 0.0
      if float(row[header["Feat51"]]) > 0.0755:
        if float(row[header["Feat28"]]) <= 0.125:
          return 1.0
        if float(row[header["Feat28"]]) > 0.125:
          return 0.0
    if float(row[header["Feat23"]]) > 10.795:
      if float(row[header["Feat36"]]) <= 0.385:
        if float(row[header["Feat9"]]) <= 0.375:
          return 1.0
        if float(row[header["Feat9"]]) > 0.375:
          return 1.0
      if float(row[header["Feat36"]]) > 0.385:
        if float(row[header["Feat0"]]) <= 0.735:
          return 1.0
        if float(row[header["Feat0"]]) > 0.735:
          return 0.0
  if float(row[header["Feat24"]]) > 0.7:
    if float(row[header["Feat2"]]) <= 2.2300000000000004:
      if float(row[header["Feat34"]]) <= 0.235:
        if float(row[header["Feat29"]]) <= 0.385:
          return 0.0
        if float(row[header["Feat29"]]) > 0.385:
          return 0.0
      if float(row[header["Feat34"]]) > 0.235:
        if float(row[header["Feat27"]]) <= 0.675:
          return 0.0
        if float(row[header["Feat27"]]) > 0.675:
          return 0.0
    if float(row[header["Feat2"]]) > 2.2300000000000004:
      if float(row[header["Feat36"]]) <= 4.695:
        if float(row[header["Feat50"]]) <= 0.10300000000000001:
          return 0.0
        if float(row[header["Feat50"]]) > 0.10300000000000001:
          return 0.0
      if float(row[header["Feat36"]]) > 4.695:
        if float(row[header["Feat31"]]) <= 0.48:
          return 0.0
        if float(row[header["Feat31"]]) > 0.48:
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
