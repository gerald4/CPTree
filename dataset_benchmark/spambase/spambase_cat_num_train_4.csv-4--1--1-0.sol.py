import csv
import sys
import os

train = "spambase_cat_num_train_4.csv"
test = "spambase_cat_num_test_4.csv"
def predict(row,header):
  if float(row[header["Feat26"]]) <= 0.20500000000000002:
    if float(row[header["Feat45"]]) <= 0.485:
      if float(row[header["Feat52"]]) <= 0.0895:
        if float(row[header["Feat51"]]) <= 0.1175:
          return 0.0
        if float(row[header["Feat51"]]) > 0.1175:
          return 1.0
      if float(row[header["Feat52"]]) > 0.0895:
        if float(row[header["Feat11"]]) <= 6.154999999999999:
          return 1.0
        if float(row[header["Feat11"]]) > 6.154999999999999:
          return 1.0
    if float(row[header["Feat45"]]) > 0.485:
      if float(row[header["Feat23"]]) <= 11.125:
        if float(row[header["Feat50"]]) <= 0.267:
          return 0.0
        if float(row[header["Feat50"]]) > 0.267:
          return 0.0
      if float(row[header["Feat23"]]) > 11.125:
        if float(row[header["Feat31"]]) <= 2.38:
          return 0.0
        if float(row[header["Feat31"]]) > 2.38:
          return 1.0
  if float(row[header["Feat26"]]) > 0.20500000000000002:
    if float(row[header["Feat0"]]) <= 1.2349999999999999:
      if float(row[header["Feat31"]]) <= 2.38:
        if float(row[header["Feat21"]]) <= 2.245:
          return 0.0
        if float(row[header["Feat21"]]) > 2.245:
          return 0.0
      if float(row[header["Feat31"]]) > 2.38:
        if float(row[header["Feat3"]]) <= 0.56:
          return 0.0
        if float(row[header["Feat3"]]) > 0.56:
          return 1.0
    if float(row[header["Feat0"]]) > 1.2349999999999999:
      if float(row[header["Feat23"]]) <= 1.0350000000000001:
        if float(row[header["Feat3"]]) <= 0.56:
          return 0.0
        if float(row[header["Feat3"]]) > 0.56:
          return 0.0
      if float(row[header["Feat23"]]) > 1.0350000000000001:
        if float(row[header["Feat1"]]) <= 0.635:
          return 0.0
        if float(row[header["Feat1"]]) > 0.635:
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
