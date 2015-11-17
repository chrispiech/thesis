import csv
import numpy as np
from scipy.interpolate import *

NUM_ROWS = 101
IN_FILE = 'raw-prior.csv'
OUT_FILE = 'interpolated-prior.csv'

def run():
	x, values, header = extract(IN_FILE)
	newX = np.linspace(0, 1, NUM_ROWS)
	newValues = interpolate(x, newX, values)
	output(newX, newValues, header)

def interpolate(x, newX, values):
	oldCols = values.shape[1]
	oldRows = values.shape[0]
	newRows = newX.shape[0]
	newValues = np.zeros((newRows, oldCols))

	for c in range(oldCols):
		y = values[:, c]
		spl = InterpolatedUnivariateSpline(x, y,k=2)
		#spl.set_smoothing_factor(0.1)
		newCol = spl(newX)
		for r in range(newRows):
			newValues[r][c] = max(0, newCol[r])
	return newValues

def output(x, values, header):
	with open(OUT_FILE, 'wb') as outfile:
		writer = csv.writer(outfile)
		writer.writerow(header)
		for r in range(x.shape[0]):
			row = []
			row.append(x[r])
			for c in range(values.shape[1]):
				row.append(values[r][c])
			writer.writerow(row)


def extract(fileName):
	x = None
	values = None
	header = None
	numCols = 0

	# create the variables based on number of lines
	with open(fileName, 'rU') as csvfile:
		lines = csvfile.readlines()
		numRows = len(lines) - 1
		numCols = len(lines[0].split(',')) - 1
		x = np.zeros((numRows,1))
		values = np.zeros((numRows, numCols))

	with open(fileName, 'rU') as csvfile:
		seenHeader = False
		reader = csv.reader(csvfile)
		r = 0
		for row in reader:
			if not seenHeader:
				seenHeader = True
				header = row
			else:
				x[r - 1] = float(row[0])
				for c in range(numCols):
					values[r - 1][c] = float(row[c + 1])
			r += 1
		header[0] = 'x'
		return x, values, header

run()




