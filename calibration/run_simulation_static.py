import pickle 
import numpy as np
import pandas as pd
import argparse
import sys


from calibration_RMSE import experiment as experiment_t

A = np.array([[0.02940123, 0.01138308, 0.02935103],
		[0.02958333, 0.01130556, 0.02947778],
		[0.03      , 0.011     , 0.0294    ],
		[0.02385223, 0.00952549, 0.02614507],
		[0.04478056, 0.01204282, 0.03185417],
		[0.04522626, 0.01195731, 0.03151456],
		[0.0455    , 0.01166667, 0.03135   ],
		[0.03    , 0.011957, 0.031515],
		[0.02357202, 0.01064115, 0.03483618],
		[0.02769547, 0.01023282, 0.03054143],
		[0.02833333, 0.01003704, 0.02856591],
		[0.02697687, 0.01303429, 0.0385675 ],
		[0.02802451, 0.01277361, 0.03221521],
		[0.02966873, 0.01164397, 0.03211438] ,
		[0.037398 ,  0.010652 , 0.036342],
		[0.032604 ,  0.012396 , 0.030682],
		[0.034905 ,  0.011540 , 0.034525],
		[0.030611 ,  0.013039  , 0.031093],
		[0.034905  , 0.011540 , 0.040000],
		[0.033742  , 0.011732 , 0.036000],
		[0.042000  , 0.012117 , 0.036000],
		[0.041481  , 0.012651 , 0.032593],
		[0.043920  , 0.012874 , 0.028176],
		[0.044938  , 0.012300 , 0.032412],
		[0.042518  , 0.012335 , 0.033408]])


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Basic Simulation')

	parser.add_argument("-cat", "--Category", default = 'all', type=str, help="Category of Input Data, default is all")
	parser.add_argument("-s", "--Start", default = '2020-08-17', type=str, help="First Date of Simulation")
	#parser.add_argument("-p", "--transmission",type=float, help="Trans Probability", required=True) # Required
	parser.add_argument("-sp", "--step_pol",type=int, help="first valid date of pol", required=True) # Required
	#parser.add_argument("-y", "--y", type=float, help="First Outside infection Rate", required = True) # Required
	#parser.add_argument("-x", "--x", type=float, help="Second Outside infection Rate", required = True) # Required
	parser.add_argument("-epoch", "--Epoch",default=15,type=int, help="Iteration Number for the model")
	parser.add_argument("-days", "--Days",default=42,type=int, help="Length of Simulaiton") 
	args = parser.parse_args()

	cat = args.Category
	start_date = args.Start
	#p = args.transmission
	sp = args.step_pol
	#y =args.y
	#x = args.x
	epoch =  args.Epoch
	days = args.Days
    
	for row in A:

		p = row[0]

		I_asym = row[1]

		alpha = row[2]
            
		experiment_t(cat, sp, p, I_asym, alpha, epoch, start_date, days)

