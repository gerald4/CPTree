
import learn_class_bin as lcb


#path1 = 'D:\Sicco\Dropbox\Dropbox\INFORMS-J-Optimization\dataset-cg-paper'
#path1 = 'D:\Sicco\Dropbox\Dropbox\INFORMS-J-Optimization\data-exp'

#for filename in os.listdir(path2):

datasets =["balance_scale", "banknote_authentication", "biodeg", "car", "credit_approval", "hepatitis",
		   "ionosphere", "iris", "mammographic_masses", "monk1", "monk2", "monk3", "pima_indian_diabetes",
		   "post_operative_patient", "seismic", "spambase", "spect_heart", "thoracy_surgery", "tic_tac_toe",
		   "wine"]

evaluation_method = "cat_num"

for i in range(1,6):
#for filename in glob.glob(os.path.join(path1, '*.train*.csv')):
	for dataset in datasets:
		if dataset in ["monk1", "monk2", "monk3", "spect_heart"]:
			if i>=2:
				pass
			else:
				path1 = f"../dataset_benchmark/{dataset}/{dataset}_{evaluation_method}_"
				filename=path1+"train_"+str(i)+".csv"
				print(filename)
			     #lcb.main(["-f",filename, "-d", 1, "-t", 900, "-p", 300])

				for depth in range(2,5):
					   lcb.main(["-f",filename, "-d", depth, "-t", 600, "-p", 150])
			    #lcb.main(["-f",filename, "-d", 4, "-t", 3600, "-p", 600])

				#for depth in range(1,5):
			    #lcb.main(["-f",filename, "-d", 4, "-t", 600, "-p", 150, "-x", 20, "-s", 1])
			    #   lcb.main(["-f",filename, "-d", depth, "-t", 3600, "-p", 150, "-x", 10, "-s", 1])
		else:
				path1 = f"../dataset_benchmark/{dataset}/{dataset}_{evaluation_method}_"
				filename=path1+"train_"+str(i)+".csv"
				print(filename)
			     #lcb.main(["-f",filename, "-d", 1, "-t", 900, "-p", 300])

				for depth in range(2,5):
					   lcb.main(["-f",filename, "-d", depth, "-t", 600, "-p", 150])
			    #lcb.main(["-f",filename, "-d", 4, "-t", 3600, "-p", 600])

				#for depth in range(1,5):
			    #lcb.main(["-f",filename, "-d", 4, "-t", 600, "-p", 150, "-x", 20, "-s", 1])
			    #   lcb.main(["-f",filename, "-d", depth, "-t", 3600, "-p", 150, "-x", 10, "-s", 1])
