import csv
import sys
import os

train = "biodeg_cat_num_train_1.csv"
test = "biodeg_cat_num_test_1.csv"
def predict(row,header):
  if float(row[header["Feat0"]]) <= 4.785500000000001:
    if float(row[header["Feat33"]]) <= 2.5:
      if float(row[header["Feat18"]]) <= 0.5:
        if float(row[header["Feat35"]]) <= 3.5865:
          return 1.0
        if float(row[header["Feat35"]]) > 3.5865:
          return 0.0
      if float(row[header["Feat18"]]) > 0.5:
        if float(row[header["Feat0"]]) <= 5.8420000000000005:
          return 0.0
        if float(row[header["Feat0"]]) > 5.8420000000000005:
          return 1.0
    if float(row[header["Feat33"]]) > 2.5:
      if float(row[header["Feat1"]]) <= 3.6421:
        if float(row[header["Feat3"]]) <= 2.5:
          return 0.0
        if float(row[header["Feat3"]]) > 2.5:
          return 0.0
      if float(row[header["Feat1"]]) > 3.6421:
        if float(row[header["Feat1"]]) <= 4.7364999999999995:
          return 1.0
        if float(row[header["Feat1"]]) > 4.7364999999999995:
          return 0.0
  if float(row[header["Feat0"]]) > 4.785500000000001:
    if float(row[header["Feat11"]]) <= -0.8294999999999999:
      if float(row[header["Feat0"]]) <= 3.9765:
        if float(row[header["Feat0"]]) <= 4.875500000000001:
          return 1.0
        if float(row[header["Feat0"]]) > 4.875500000000001:
          return 1.0
      if float(row[header["Feat0"]]) > 3.9765:
        if float(row[header["Feat38"]]) <= 8.7415:
          return 1.0
        if float(row[header["Feat38"]]) > 8.7415:
          return 0.0
    if float(row[header["Feat11"]]) > -0.8294999999999999:
      if float(row[header["Feat3"]]) <= 2.5:
        if float(row[header["Feat4"]]) <= 6.5:
          return 0.0
        if float(row[header["Feat4"]]) > 6.5:
          return 0.0
      if float(row[header["Feat3"]]) > 2.5:
        if float(row[header["Feat19"]]) <= 0.5:
          return 0.0
        if float(row[header["Feat19"]]) > 0.5:
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
