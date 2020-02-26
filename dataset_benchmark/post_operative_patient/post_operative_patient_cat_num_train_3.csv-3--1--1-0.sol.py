import csv
import sys
import os

train = "post_operative_patient_cat_num_train_3.csv"
test = "post_operative_patient_cat_num_test_3.csv"
def predict(row,header):
  if float(row[header["L-CORE_high"]]) <= 0.5:
    if float(row[header["CORE-STBL_stable"]]) <= 0.5:
      if float(row[header["BP-STBL_stable"]]) <= 0.5:
        return 0.0
      if float(row[header["BP-STBL_stable"]]) > 0.5:
        return 2.0
    if float(row[header["CORE-STBL_stable"]]) > 0.5:
      if float(row[header["COMFORT_7.0"]]) <= 0.5:
        return 0.0
      if float(row[header["COMFORT_7.0"]]) > 0.5:
        return 2.0
  if float(row[header["L-CORE_high"]]) > 0.5:
    if float(row[header["BP-STBL_unstable"]]) <= 0.5:
      if float(row[header["BP-STBL_stable"]]) <= 0.5:
        return 0.0
      if float(row[header["BP-STBL_stable"]]) > 0.5:
        return 2.0
    if float(row[header["BP-STBL_unstable"]]) > 0.5:
      if float(row[header["L-SURF_low"]]) <= 0.5:
        return 0.0
      if float(row[header["L-SURF_low"]]) > 0.5:
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
