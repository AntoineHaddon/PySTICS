# to load outputs
import pandas as pd

# to read .xml files
import xml.etree.ElementTree as ET

# to run simulation with command line executable JavaSticsCmd.exe
import subprocess as sproc



class usm():
	""" Class corresponding to a STICS usm (unit of simulation) with utilities to run simulations, change inputs and read output files. 
		Initialized with the directory containing the usm and name
		Directory containing the JavaSTICS executable (JavaSticsCmd.exe) needs to be given to run simulations
	"""

	# initialization
	def __init__(self, dirUSM, name, JavaSticsDir=None):
		# directory containing the usm
		self.dirUSM = dirUSM

		# Directory containing the JavaSTICS executable (JavaSticsCmd.exe)
		# Needed to run simulations
		self.JavaSticsDir = JavaSticsDir

		# USM name
		self.name = name

		# output files
		self.varModFile = self.dirUSM + 'var.mod' # file with list of outputs
		self.mod_s = self.dirUSM + 'mod_s' + self.name + '.sti' # file with output data







	###############
	## rum STICS
	##############

	def run(self):
		""" Run STICS simulation """
		return sproc.run(["java", "-jar", "JavaSticsCmd.exe", "--run", self.dirUSM, self.name], cwd=self.JavaSticsDir)






	#####################
	# Files utilities
	#####################


	def get_ftec(self):
		""" Return name of crop management file (***_tec.xml) """

		##### read usms.xml file
		usmTree = ET.parse(self.dirUSM + 'usms.xml')

		# find node corrsponding to usm
		for elem in usmTree.getroot():
			if elem.attrib['nom'] == self.name:
				nodeUsm = elem 

		### find tec file of first crop
		for elem in nodeUsm.findall('plante'):
			if elem.attrib['dominance']=='1':
				return self.dirUSM + elem.findall('ftec')[0].text




	def set_IniFile(self,initFile):
		""" set initialisation file by modifying usms.xml file """

		##### read  usms.xml file
		usmTree = ET.parse(self.dirUSM + 'usms.xml')

		# find node corrsponding to usm
		for elem in usmTree.getroot():
			if elem.attrib['nom'] == self.name:
				nodeUsm = elem

		# change initFile
		for elem in nodeUsm.findall('finit'):
			elem.text = initFile

		##### write file
		usmTree.write(self.dirUSM +"usms.xml")



	######################## 
	##  Outputs utilities
	########################

	def loadData(self,index='jul'):
		""" Returns a pandas DataFrame version of mod_s file
		same structure as mod_s**.sti file : on each line outputs for a day """
		return pd.read_csv(self.mod_s, sep=';',index_col=index)






	########################
	# Parameters utilities
	########################

	def loadSoilParam(self):
		""" load soil layers parameters in a pandas dataframe"""
		paramsolFile = self.dirUSM + 'param.sol'
		
		### load file, removing first lines to have only parameters of layers
		soilParam = pd.read_csv(paramsolFile, sep=' ',header=None, skiprows=3, usecols=range(8,16))
		soilParam.set_index(pd.Index(range(1,6)), inplace=True) 

		### rename columns with parameter names
		soilParam.rename(columns={8:'thickness', 9:'hccf', 10:'hminf', 11:'bulkDensity'}, inplace=True)

		return soilParam







	######################
	## Write inputs
	#####################


	def addIrrigIntervention(self,nodeIrrigCal,irrigIntervention):
		""" add an irrigation intervention at node in xml tree """
		##### create new irrigation event
		newIntervention = ET.SubElement(nodeIrrigCal, 'intervention', attrib={'nb_colonnes': '2'} )
		Date = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'julapI_or_sum_upvt'} )
		Date.text = str(int(irrigIntervention[0]))
		Amount = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'amount'} )
		Amount.text = str(irrigIntervention[1])
		## for formatting of file
		newIntervention.tail = "\n" + 20*" "
		newIntervention.text = "\n" + 22*" "
		Date.tail = "\n" + 22*" "



	def writeIrrigCal(self,irrigCal):
		""" write irrigation dates and amounts in crop management file (_tec.xml file) for STICS
			irrigCal is an 2d numpy array with each line is an irrigation intervention with first element is date (julian) and second element is irrigation volume (in mm)
			i.e. : irrigCal = [ [ date1, amount1], [date2, amount2], ... ] """

		##### read  _tec.xml file
		cropmgntTree = ET.parse(self.get_ftec() )

		#### irrigation part of file
		for elem in cropmgntTree.getroot():
			if elem.attrib['nom']=='irrigation':
				nodeIrrig = elem

		### set irrigation with calendar (i.e deactivate calculation of irrigation by stics)
		### i.e. need line <option choix="2" nom="automatic calculation of irrigations" nomParam="codecalirrig">
		for elem in nodeIrrig.iter('option'):
			if elem.attrib['nomParam'] == 'codecalirrig':
				elem.attrib['choix'] = '2'

		## calendar of irrigation events
		for elem in nodeIrrig.iter('ta'):
			nodeIrrigCal = elem

		######## setting number of irrigation events
		nodeIrrigCal.set('nb_interventions', str( irrigCal.shape[0] ) )

		####### remove old irrigation events
		for irrigIntervention in nodeIrrigCal.findall('intervention'):
			nodeIrrigCal.remove(irrigIntervention)

		### add events
		for indexIrrig in range(irrigCal.shape[0]):
			self.addIrrigIntervention(nodeIrrigCal, irrigCal[indexIrrig] )

		##### write file
		cropmgntTree.write(self.get_ftec())




	def addFertiIntervention(self,nodeFertiCal,fertiIntervention):
		""" add an fertilisation intervention at node in xml tree """
		##### create new fertilisation event
		newIntervention = ET.SubElement(nodeFertiCal, 'intervention', attrib={'nb_colonnes': '2'} )
		Date = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'julapN_or_sum_upvt'} )
		Date.text = str(int(fertiIntervention[0]))
		Amount = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'absolute_value/%'} )
		Amount.text = str(fertiIntervention[1])
		## for formatting of file
		newIntervention.tail = "\n" + 20*" "
		newIntervention.text = "\n" + 22*" "
		Date.tail = "\n" + 22*" "


	def writeFertiCal(self,fertiCal,fertiType=None):
		""" write fertilisation dates and amounts in crop management file for STICS
			fertiCal is a 2d numpy array with each line is an fertilisation intervention with first element is date (julian) and second element is fertilisation ammout [kg/ha]
			i.e. : fertiCal = [ [ date1, amount1], [date2, amount2], ... ] """

		##### read  _tec.xml file
		cropmgntTree = ET.parse(self.get_ftec() )

		#### fertilisation part of file
		for elem in cropmgntTree.getroot():
			if elem.attrib['nom']=='fertilisation':
				nodeFerti = elem

		#set fertilizer type
		if not fertiType is None:
			for elem in nodeFerti:
				if elem.attrib['nom']=='engrais':
					elem.text = str(fertiType)

		## calendar of fertilisation events
		nodeFertiCal = nodeFerti.find('ta')

		######## setting number of ferti events
		nodeFertiCal.set('nb_interventions', str( fertiCal.shape[0] ) )

		####### remove old ferti events
		for fertiIntervention in nodeFertiCal.findall('intervention'):
			nodeFertiCal.remove(fertiIntervention)

		### add events
		for indexFerti in range(fertiCal.shape[0]):
			self.addFertiIntervention(nodeFertiCal, fertiCal[indexFerti] )

		##### write file
		cropmgntTree.write(self.get_ftec())



