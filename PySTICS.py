# import numpy as np

# for load outputs
import pandas as pd

# to read .xml files
import xml.etree.ElementTree as ET

import datetime as dt

# to run simulation with command line executable JavaSticsCmd.exe
import subprocess as sproc



class usm():
	""" Class containing all relevant information to a STICS usm (Unit of simulation) : directories, input and output files 
		Initialized with the directory containing the usm and name
		Directory containing the JavaSTICS executable (JavaSticsCmd.exe) needs to be given to run simulations
	"""

	# initialization
	def __init__(self, dirUSM, name, JavaSticsDir=''):
		# directory containing the usm
		self.dirUSM = dirUSM

		# Directory containing the JavaSTICS executable (JavaSticsCmd.exe)
		# Needed to run simulations
		self.JavaSticsDir = JavaSticsDir

		# USM name
		self.name = name

		# crop management file 
		self.ftec = self.dirUSM + self.name + '_tec.xml'

		# output files
		self.varModFile = self.dirUSM + 'var.mod' # file with list of outputs
		self.mod_s = self.dirUSM + 'mod_s' + self.name + '.sti' # file with output data



	def run(self):
		""" Run STICS simulation """
		return sproc.run(["java", "-jar", "JavaSticsCmd.exe", "--run", self.dirUSM, self.name], cwd=self.JavaSticsDir)


	def loadData(self):
		""" Returns a pandas DataFrame version of mod_s file
        same structure as mod_s**.sti file : on each line outputs for a day """
		return pd.read_csv(self.mod_s, sep=';')








