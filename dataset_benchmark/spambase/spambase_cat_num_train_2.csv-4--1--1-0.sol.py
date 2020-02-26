import csv
import sys
import os

train = "spambase_cat_num_train_2.csv"
test = "spambase_cat_num_test_2.csv"
def predict(row,header):
  if float(row[header["Feat52"]]) <= 0.1465:
    if float(row[header["Feat3"]]) <= 0.89:
      if float(row[header["Feat26"]]) <= 0.21000000000000002:
        if float(row[header["Feat51"]]) <= 0.1455:
          return 0.0
        if float(row[header["Feat51"]]) > 0.1455:
          return 1.0
      if float(row[header["Feat26"]]) > 0.21000000000000002:
        if float(row[header["Feat50"]]) <= 1.1735:
          return 0.0
        if float(row[header["Feat50"]]) > 1.1735:
          return 0.0
    if float(row[header["Feat3"]]) > 0.89:
      if float(row[header["Feat42"]]) <= 0.195:
        if float(row[header["Feat0"]]) <= 4.27:
          return 1.0
        if float(row[header["Feat0"]]) > 4.27:
          return 0.0
      if float(row[header["Feat42"]]) > 0.195:
        if float(row[header["Feat0"]]) <= 2.1950000000000003:
          return 0.0
        if float(row[header["Feat0"]]) > 2.1950000000000003:
          return 1.0
  if float(row[header["Feat52"]]) > 0.1465:
    if float(row[header["Feat32"]]) <= 0.515:
      if float(row[header["Feat43"]]) <= 0.09:
        if float(row[header["Feat24"]]) <= 0.565:
          return 1.0
        if float(row[header["Feat24"]]) > 0.565:
          return 0.0
      if float(row[header["Feat43"]]) > 0.09:
        if float(row[header["Feat28"]]) <= 0.475:
          return 1.0
        if float(row[header["Feat28"]]) > 0.475:
          return 1.0
    if float(row[header["Feat32"]]) > 0.515:
      if float(row[header["Feat50"]]) <= 1.1735:
        if float(row[header["Feat37"]]) <= 1.5:
          return 1.0
        if float(row[header["Feat37"]]) > 1.5:
          return 1.0
      if float(row[header["Feat50"]]) > 1.1735:
        if float(row[header["Feat13"]]) <= 2.0700000000000003:
          return 1.0
        if float(row[header["Feat13"]]) > 2.0700000000000003:
          return 1.0


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
