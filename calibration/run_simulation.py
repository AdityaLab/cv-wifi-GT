import pickle 
import numpy as np
import pandas as pd
import argparse
import sys


from calibration_RMSE_t import experiment as experiment_t

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Basic Simulation')

	parser.add_argument("-cat", "--Category", default = 'all', type=str, help="Category of Input Data, default is all")
	parser.add_argument("-s", "--Start", default = '2020-08-17', type=str, help="First Date of Simulation")
	parser.add_argument("-p", "--transmission",type=float, help="Trans Probability", required=True) # Required
	parser.add_argument("-sp", "--step_pol",type=int, help="first valid date of pol", required=True) # Required
	parser.add_argument("-y", "--y", type=float, help="First Outside infection Rate", required = True) # Required
	parser.add_argument("-x", "--x", type=float, help="Second Outside infection Rate", required = True) # Required
	parser.add_argument("-epoch", "--Epoch",default=15,type=int, help="Iteration Number for the model")
	parser.add_argument("-days", "--Days",default=42,type=int, help="Length of Simulaiton") 
	args = parser.parse_args()

	cat = args.Category
	start_date = args.Start
	p = args.transmission
	sp = args.step_pol
	y =args.y
	x = args.x
	epoch =  args.Epoch
	days = args.Days
    
    
	experiment_t(cat, sp, p, y, x, epoch, start_date, days)

