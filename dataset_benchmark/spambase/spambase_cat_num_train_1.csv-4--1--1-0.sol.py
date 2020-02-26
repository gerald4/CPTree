import csv
import sys
import os

train = "spambase_cat_num_train_1.csv"
test = "spambase_cat_num_test_1.csv"
def predict(row,header):
  if float(row[header["Feat40"]]) <= 3.57:
    if float(row[header["Feat52"]]) <= 0.026500000000000003:
      if float(row[header["Feat33"]]) <= 0.385:
        if float(row[header["Feat51"]]) <= 0.22599999999999998:
          return 0.0
        if float(row[header["Feat51"]]) > 0.22599999999999998:
          return 1.0
      if float(row[header["Feat33"]]) > 0.385:
        if float(row[header["Feat35"]]) <= 0.36:
          return 0.0
        if float(row[header["Feat35"]]) > 0.36:
          return 0.0
    if float(row[header["Feat52"]]) > 0.026500000000000003:
      if float(row[header["Feat24"]]) <= 0.365:
        if float(row[header["Feat37"]]) <= 0.13:
          return 1.0
        if float(row[header["Feat37"]]) > 0.13:
          return 1.0
      if float(row[header["Feat24"]]) > 0.365:
        if float(row[header["Feat10"]]) <= 0.485:
          return 0.0
        if float(row[header["Feat10"]]) > 0.485:
          return 0.0
  if float(row[header["Feat40"]]) > 3.57:
    if float(row[header["Feat29"]]) <= 3.41:
      if float(row[header["Feat24"]]) <= 0.485:
        if float(row[header["Feat51"]]) <= 0.4575:
          return 0.0
        if float(row[header["Feat51"]]) > 0.4575:
          return 0.0
      if float(row[header["Feat24"]]) > 0.485:
        if float(row[header["Feat13"]]) <= 0.185:
          return 0.0
        if float(row[header["Feat13"]]) > 0.185:
          return 1.0
    if float(row[header["Feat29"]]) > 3.41:
      if float(row[header["Feat56"]]) <= 3189.0:
        if float(row[header["Feat0"]]) <= 2.1950000000000003:
          return 0.0
        if float(row[header["Feat0"]]) > 2.1950000000000003:
          return 1.0
      if float(row[header["Feat56"]]) > 3189.0:
        if float(row[header["Feat40"]]) <= 3.57:
          return 1.0
        if float(row[header["Feat40"]]) > 3.57:
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
