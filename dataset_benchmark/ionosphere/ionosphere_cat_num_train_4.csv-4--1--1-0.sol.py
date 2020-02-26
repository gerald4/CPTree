import csv
import sys
import os

train = "ionosphere_cat_num_train_4.csv"
test = "ionosphere_cat_num_test_4.csv"
def predict(row,header):
  if float(row[header["Feat2"]]) <= 0.20009500000000002:
    if float(row[header["Feat27"]]) <= -0.661505:
      if float(row[header["Feat28"]]) <= 0.36682499999999996:
        if float(row[header["Feat33"]]) <= 0.129765:
          return 0.0
        if float(row[header["Feat33"]]) > 0.129765:
          return 0.0
      if float(row[header["Feat28"]]) > 0.36682499999999996:
        if float(row[header["Feat0"]]) <= 0.5:
          return 0.0
        if float(row[header["Feat0"]]) > 0.5:
          return 0.0
    if float(row[header["Feat27"]]) > -0.661505:
      if float(row[header["Feat33"]]) <= -0.29583000000000004:
        if float(row[header["Feat32"]]) <= -0.03998:
          return 0.0
        if float(row[header["Feat32"]]) > -0.03998:
          return 0.0
      if float(row[header["Feat33"]]) > -0.29583000000000004:
        if float(row[header["Feat24"]]) <= 0.90552:
          return 0.0
        if float(row[header["Feat24"]]) > 0.90552:
          return 0.0
  if float(row[header["Feat2"]]) > 0.20009500000000002:
    if float(row[header["Feat3"]]) <= -0.61903:
      if float(row[header["Feat18"]]) <= 0.6698299999999999:
        if float(row[header["Feat23"]]) <= 0.0005099999999999999:
          return 1.0
        if float(row[header["Feat23"]]) > 0.0005099999999999999:
          return 0.0
      if float(row[header["Feat18"]]) > 0.6698299999999999:
        if float(row[header["Feat15"]]) <= 0.39568500000000006:
          return 0.0
        if float(row[header["Feat15"]]) > 0.39568500000000006:
          return 0.0
    if float(row[header["Feat3"]]) > -0.61903:
      if float(row[header["Feat5"]]) <= -0.79531:
        if float(row[header["Feat0"]]) <= 0.5:
          return 0.0
        if float(row[header["Feat0"]]) > 0.5:
          return 0.0
      if float(row[header["Feat5"]]) > -0.79531:
        if float(row[header["Feat4"]]) <= 0.051515:
          return 0.0
        if float(row[header["Feat4"]]) > 0.051515:
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
