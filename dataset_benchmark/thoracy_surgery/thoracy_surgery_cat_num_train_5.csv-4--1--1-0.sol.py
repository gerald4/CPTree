import csv
import sys
import os

train = "thoracy_surgery_cat_num_train_5.csv"
test = "thoracy_surgery_cat_num_test_5.csv"
def predict(row,header):
  if float(row[header["FVC"]]) <= 4.34:
    if float(row[header["DGN_DGN5"]]) <= 0.5:
      if float(row[header["Dyspnoea.Before_T"]]) <= 0.5:
        if float(row[header["DGN_DGN8"]]) <= 0.5:
          return 0.0
        if float(row[header["DGN_DGN8"]]) > 0.5:
          return 1.0
      if float(row[header["Dyspnoea.Before_T"]]) > 0.5:
        if float(row[header["Perform.Status_PRZ1"]]) <= 0.5:
          return 1.0
        if float(row[header["Perform.Status_PRZ1"]]) > 0.5:
          return 0.0
    if float(row[header["DGN_DGN5"]]) > 0.5:
      if float(row[header["FVC"]]) <= 3.1950000000000003:
        if float(row[header["Cough.Before_T"]]) <= 0.5:
          return 0.0
        if float(row[header["Cough.Before_T"]]) > 0.5:
          return 1.0
      if float(row[header["FVC"]]) > 3.1950000000000003:
        if float(row[header["Hamemoptysis.Before_T"]]) <= 0.5:
          return 1.0
        if float(row[header["Hamemoptysis.Before_T"]]) > 0.5:
          return 0.0
  if float(row[header["FVC"]]) > 4.34:
    if float(row[header["FVC"]]) <= 4.619999999999999:
      if float(row[header["Dyspnoea.Before_T"]]) <= 0.5:
        if float(row[header["size.Orign.Tumour_OC13"]]) <= 0.5:
          return 0.0
        if float(row[header["size.Orign.Tumour_OC13"]]) > 0.5:
          return 1.0
      if float(row[header["Dyspnoea.Before_T"]]) > 0.5:
        if float(row[header["FVC"]]) <= 3.78:
          return 0.0
        if float(row[header["FVC"]]) > 3.78:
          return 1.0
    if float(row[header["FVC"]]) > 4.619999999999999:
      if float(row[header["Age"]]) <= 66.5:
        if float(row[header["DGN_DGN5"]]) <= 0.5:
          return 0.0
        if float(row[header["DGN_DGN5"]]) > 0.5:
          return 1.0
      if float(row[header["Age"]]) > 66.5:
        if float(row[header["FVC"]]) <= 3.1950000000000003:
          return 0.0
        if float(row[header["FVC"]]) > 3.1950000000000003:
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
